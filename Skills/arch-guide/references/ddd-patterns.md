---
name: ddd-patterns
description: Padrões táticos de DDD — Entity, Value Object, Aggregate, Repository, Domain Event, Domain Service e quando usar cada um.
---

# Padrões Táticos de DDD

## Entity (Entidade)

**Definição:** Um objeto com identidade única que persiste através de mudanças de estado.

**Características:**
- Tem um ID (UUID, int, específico do domínio)
- Duas entidades com o mesmo ID são a mesma entidade, mesmo que seus atributos sejam diferentes
- Mutável — seu estado muda ao longo do ciclo de vida
- Contém comportamento (métodos), não apenas dados

**Quando usar:** O conceito tem um ciclo de vida e você precisa rastreá-lo ao longo do tempo.

**Exemplos:** `Pedido`, `Cliente`, `Fatura`, `Produto`, `Assinatura`, `Tarefa`

**Uso incorreto:** Usar uma Entity quando o conceito não tem identidade significativa (use Value Object em vez disso).

```typescript
// Correto
class Tarefa {
  private readonly id: TarefaId;
  private status: StatusTarefa;
  private titulo: string;

  concluir(): void {
    if (this.status === StatusTarefa.CONCLUIDA) throw new ErroDominio('Tarefa já concluída');
    this.status = StatusTarefa.CONCLUIDA;
    this.adicionarEvento(new TarefaConcluida(this.id));
  }
}
```

---

## Value Object (Objeto de Valor)

**Definição:** Um objeto definido inteiramente por seus atributos, sem identidade.

**Características:**
- Imutável — uma vez criado, não pode mudar
- Dois Value Objects com os mesmos atributos são iguais
- Sem ID
- Contém comportamento relevante para o valor que representa

**Quando usar:** O conceito é descritivo e intercambiável se os atributos forem iguais.

**Exemplos:** `Dinheiro`, `EnderecoEmail`, `Telefone`, `IntervaloDatas`, `Endereco`, `StatusTarefa`

**Uso incorreto:** Tornar um Value Object mutável via setters — anula o propósito.

```typescript
// Correto
class Dinheiro {
  constructor(
    private readonly valor: number,
    private readonly moeda: string,
  ) {
    if (valor < 0) throw new ErroDominio('Valor não pode ser negativo');
  }

  somar(outro: Dinheiro): Dinheiro {
    if (outro.moeda !== this.moeda) throw new ErroDominio('Moedas incompatíveis');
    return new Dinheiro(this.valor + outro.valor, this.moeda); // retorna novo, imutável
  }

  equals(outro: Dinheiro): boolean {
    return this.valor === outro.valor && this.moeda === outro.moeda;
  }
}
```

---

## Aggregate (Agregado)

**Definição:** Um cluster de objetos de domínio (entidades + VOs) tratado como uma única unidade para mudanças de dados. O Aggregate Root é o único ponto de entrada para todas as modificações.

**Características:**
- Tem uma Entity raiz (o Aggregate Root)
- Objetos externos referenciam apenas o Aggregate Root, nunca entidades internas
- O root é responsável por manter invariantes em todos os objetos do aggregate
- Fronteira de persistência: carregado e salvo como uma unidade inteira

**Quando usar:** Múltiplas entidades devem mudar juntas para manter consistência.

**A regra:** Apenas o Aggregate Root pode ser referenciado de fora. Nunca mantenha referência direta a uma entidade interna de um aggregate a partir de fora.

**Orientação de tamanho:** Mantenha aggregates pequenos. Aggregates grandes causam contenção de lock. Se dois conceitos não precisam mudar juntos atomicamente, pertencem a aggregates separados.

```typescript
// Lista é o Aggregate Root
class Lista {
  private itens: ItemLista[]; // entidade interna — não acessível de fora

  adicionarItem(titulo: string, prioridade: Prioridade): void {
    // Lista aplica o invariante: máximo 100 itens
    if (this.itens.length >= 100) throw new ErroDominio('Lista atingiu o limite de itens');
    this.itens.push(new ItemLista(titulo, prioridade));
  }
}

// Correto: acesso pelo root
lista.adicionarItem('Comprar leite', Prioridade.MEDIA);

// Errado: bypassar o root
lista.itens.push(new ItemLista(...)); // quebra invariantes
```

---

## Repository (Repositório)

**Definição:** Uma interface tipo coleção na camada Domain que abstrai a persistência. Implementações ficam no Infrastructure.

**Características:**
- Interface definida em `domain/` — sem imports de infrastructure
- Parece uma coleção em memória: `adicionar()`, `remover()`, `buscarPorId()`, `buscarPor...()`
- Trabalha apenas com Aggregate Roots — nunca com entidades internas individuais
- Implementação em `infrastructure/` conhece o ORM/banco

**Quando usar:** Você precisa carregar ou salvar objetos de domínio.

**Regra crítica:** A interface de Repositório não deve mencionar o ORM, banco ou SQL. É uma abstração de domínio.

```typescript
// domain/tarefa/TarefaRepository.ts — apenas interface, sem imports
interface TarefaRepository {
  buscarPorId(id: TarefaId): Promise<Tarefa | null>;
  buscarPorLista(listaId: ListaId): Promise<Tarefa[]>;
  salvar(tarefa: Tarefa): Promise<void>;
  remover(id: TarefaId): Promise<void>;
}

// infrastructure/tarefa/PrismaTarefaRepository.ts — conhece o Prisma
class PrismaTarefaRepository implements TarefaRepository {
  constructor(private prisma: PrismaClient) {}

  async buscarPorId(id: TarefaId): Promise<Tarefa | null> {
    const linha = await this.prisma.tarefa.findUnique({ where: { id: id.valor } });
    return linha ? this.paraDominio(linha) : null;
  }
  // ...
}
```

---

## Domain Event (Evento de Domínio)

**Definição:** Um registro de algo que aconteceu no domínio. Imutável. Nome no tempo passado.

**Características:**
- Valor imutável: criado uma vez, nunca modificado
- Nome no tempo passado (`TarefaConcluida`, não `ConcluirTarefa`)
- Contém todos os dados necessários para entender o que aconteceu
- Lançado por Aggregate Roots durante mudanças de estado
- Consumido pela camada Application para disparar efeitos colaterais (e-mails, projeções, outros Use Cases)

**Quando usar:** Uma mudança de estado no domínio é significativa para outras partes do sistema.

**Onde despachar:** A camada Application despacha eventos (não os objetos de domínio). Objetos de domínio os lançam internamente; Use Cases os despacham via event bus.

```typescript
// domain/tarefa/events/TarefaConcluida.ts
class TarefaConcluida {
  readonly ocorridoEm: Date;
  constructor(
    readonly tarefaId: TarefaId,
    readonly listaId: ListaId,
    readonly concluidoPor: UsuarioId,
  ) {
    this.ocorridoEm = new Date();
  }
}

// application/tarefa/ConcluirTarefaUseCase.ts
class ConcluirTarefaUseCase {
  async executar(dto: ConcluirTarefaDto): Promise<void> {
    const tarefa = await this.tarefaRepository.buscarPorId(new TarefaId(dto.tarefaId));
    tarefa.concluir();
    await this.tarefaRepository.salvar(tarefa);
    await this.eventBus.publicar(tarefa.extrairEventos()); // despacha após salvar
  }
}
```

---

## Domain Service (Serviço de Domínio)

**Definição:** Um serviço sem estado na camada Domain que expressa uma operação de domínio que não pertence naturalmente a uma entidade.

**Características:**
- Sem estado (nenhum estado de instância)
- Opera apenas sobre objetos de domínio
- NÃO chama repositórios (isso é camada Application)
- NÃO depende de infrastructure

**Quando usar:** A operação envolve múltiplos objetos de domínio mas não se encaixa em nenhuma entidade específica.

**Erro comum:** Colocar toda a lógica em Domain Services em vez de entidades → leva a modelo de domínio anêmico. Prefira entidades ricas. Use Domain Services apenas quando a operação verdadeiramente abrange múltiplos aggregates e pertence ao domínio, não à application.

```typescript
// domain/tarefa/ServicoOrdenacao.ts
class ServicoOrdenacao {
  // Envolve tanto Lista quanto Tarefa — não pertence naturalmente a nenhum dos dois
  reordenar(lista: Lista, tarefas: Tarefa[], novaOrdem: TarefaId[]): void {
    if (novaOrdem.length !== tarefas.length) throw new ErroDominio('Ordem inválida');
    lista.aplicarOrdem(novaOrdem);
  }
}
```

---

## Árvore de Decisão: Qual Padrão?

```
O conceito é significativo no domínio do negócio?
  Não → é preocupação de infrastructure/application, não um objeto de domínio
  Sim ↓

Tem identidade única que persiste ao longo do tempo?
  Sim → Entity (ou Aggregate Root se é uma fronteira de consistência)
  Não → Value Object

É uma Entity que possui outras entidades e aplica invariantes entre elas?
  Sim → Aggregate Root
  Não → Entity simples

É algo que aconteceu, não algo que existe?
  Sim → Domain Event

É uma operação sem estado que abrange múltiplas entidades e pertence ao domínio?
  Sim → Domain Service
  Não → o comportamento pertence à própria entidade

Representa "uma coleção de aggregates no banco de dados"?
  Sim → Interface de Repositório (domain) + implementação (infrastructure)
```
