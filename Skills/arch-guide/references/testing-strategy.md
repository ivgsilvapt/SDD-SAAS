---
name: testing-strategy
description: Abordagem de testes por camada — o que testar, como testar e quais ferramentas usar em cada camada da Clean Architecture.
---

# Estratégia de Testes por Camada

## Camada Domain — Testes Unitários Puros

**O que testar:**
- Invariantes de entidades (regras que devem sempre ser verdadeiras)
- Igualdade e imutabilidade de Value Objects
- Regras de consistência de Aggregates
- Cálculos de Domain Services
- Emissão de Domain Events em mudanças de estado

**Como testar:**
- Instancie objetos de domínio diretamente — sem mocks, sem container de DI
- Teste via métodos públicos que representam comportamentos de domínio
- Verifique estado chamando métodos de consulta ou inspecionando eventos emitidos

**O que NÃO fazer:**
- Mockar o banco para "testar lógica de domínio" — o domínio não tem dependência de banco
- Chamar código HTTP ou de Infrastructure a partir de testes de domínio
- Pular testes de domínio porque "está coberto por testes de integração" — testes de domínio são os mais rápidos e confiáveis

**Exemplo de padrão:**
```typescript
describe('Tarefa', () => {
  it('emite TarefaConcluida ao ser concluída', () => {
    const tarefa = Tarefa.criar(listaId, 'Comprar leite');
    tarefa.concluir();
    expect(tarefa.extrairEventos()).toContainEqual(new TarefaConcluida(tarefa.id));
  });

  it('lança erro ao concluir tarefa já concluída', () => {
    const tarefa = Tarefa.criar(listaId, 'Comprar leite');
    tarefa.concluir();
    expect(() => tarefa.concluir()).toThrow('Tarefa já concluída');
  });
});
```

---

## Camada Application — Testes Unitários com Mocks de Repositório

**O que testar:**
- Caminhos felizes dos Use Cases
- Caminhos de erro dos Use Cases (entidade não encontrada, falhas de validação)
- Sequência correta de orquestração (carregar → chamar → salvar → publicar eventos)

**Como testar:**
- Injete implementações de Repositório in-memory ou fake (não o banco real)
- Injete um EventBus mock
- NÃO use banco de dados real, HTTP ou sistema de arquivos

**Por que fakes em vez de mocks:** Fakes (implementações in-memory) são mais resilientes do que stubs de objetos mock. Construa um `TarefaRepositoryEmMemoria` simples uma vez e reutilize em todos os testes de Use Cases de Tarefa.

**Exemplo de padrão:**
```typescript
describe('ConcluirTarefaUseCase', () => {
  it('salva tarefa e publica TarefaConcluida', async () => {
    const repo = new TarefaRepositoryEmMemoria();
    const eventBus = new EventBusFake();
    const tarefa = Tarefa.criar(listaId, 'Comprar leite');
    await repo.salvar(tarefa);

    const useCase = new ConcluirTarefaUseCase(repo, eventBus);
    await useCase.executar({ tarefaId: tarefa.id.valor });

    const tarefaSalva = await repo.buscarPorId(tarefa.id);
    expect(tarefaSalva.status).toBe(StatusTarefa.CONCLUIDA);
    expect(eventBus.publicados).toContainEqual(
      expect.objectContaining({ tipo: 'TarefaConcluida' })
    );
  });
});
```

---

## Camada Infrastructure — Testes de Integração (Dependências Reais)

**O que testar:**
- Implementações de Repositório: salvar, carregar, consultar por filtros
- HTTP clients externos: formato de request, parsing de response
- Adapters de message broker: publicar e consumir

**Como testar:**
- Use um banco de dados real (test container, SQLite in-memory, ou banco de teste dedicado)
- Nunca mocke o banco em testes de infrastructure — isso anula o propósito
- Isole os testes: cada teste começa com estado limpo de banco (truncar ou rollback de transação)
- Teste o mapeamento banco-para-domínio: o que você salva deve voltar intacto

**O que NÃO fazer:**
- Testar lógica de negócio aqui — lógica de negócio pertence a testes de domínio
- Usar credenciais de produção — use um ambiente de teste dedicado

**Exemplo de padrão:**
```typescript
describe('PrismaTarefaRepository', () => {
  beforeEach(() => truncarTodasTabelas(prisma));

  it('retorna null para id desconhecido', async () => {
    const repo = new PrismaTarefaRepository(prisma);
    expect(await repo.buscarPorId(new TarefaId('desconhecido'))).toBeNull();
  });

  it('persiste e recupera uma tarefa corretamente', async () => {
    const tarefa = Tarefa.criar(listaId, 'Comprar leite');
    await repo.salvar(tarefa);
    const carregada = await repo.buscarPorId(tarefa.id);
    expect(carregada.titulo).toBe('Comprar leite');
    expect(carregada.id).toEqual(tarefa.id);
  });
});
```

---

## Camada Presentation — Testes E2E / Integração HTTP

**O que testar:**
- Handlers de rota: status codes, estrutura do corpo da resposta, respostas de erro
- Validação de entrada: campos ausentes, formatos inválidos retornam 400
- Aplicação de autenticação: requisições não autenticadas retornam 401
- Caminho feliz para cada endpoint

**Como testar:**
- Inicie o servidor real (ou use um cliente de teste que monta a aplicação)
- Use banco real (ou in-memory pré-populado) — sem mocks neste nível
- Teste via HTTP: envie requests, verifique responses

**O que NÃO testar aqui:**
- Lógica de negócio — já coberta pelos testes de domínio e application
- Casos extremos detalhados — pertencem ao nível de domínio/application

**Exemplo de padrão:**
```typescript
describe('POST /tarefas', () => {
  it('retorna 201 e id da tarefa em request válido', async () => {
    const response = await cliente.post('/tarefas').send(payloadValido);
    expect(response.status).toBe(201);
    expect(response.body.id).toBeDefined();
  });

  it('retorna 400 quando título está ausente', async () => {
    const response = await cliente.post('/tarefas').send({ listaId: 'l1' });
    expect(response.status).toBe(400);
  });
});
```

---

## Pirâmide de Testes — Resumo

```
       /\
      /  \    E2E (poucos, lentos, caros)
     /    \   → Camada Presentation: endpoints HTTP, auth, roteamento
    /──────\
   /        \  Integração (moderados, velocidade média)
  /          \ → Camada Infrastructure: round-trips de Repositório, adapters externos
 /────────────\
/              \ Unitários (muitos, rápidos, baratos)
/──────────────\ → Camada Domain: invariantes, regras de negócio
                  Camada Application: orquestração de Use Cases (repos fake)
```

**Proporções práticas:** ~60% unitários (domain + application), ~30% integração (infrastructure), ~10% E2E (presentation).

---

## Convenção de Pastas

```
tests/
├── unit/
│   ├── domain/         ← testes puros de domínio
│   └── application/    ← testes de Use Case com repos fake
├── integration/
│   └── infrastructure/ ← testes de repositório com banco real
└── e2e/
    └── presentation/   ← testes de endpoint HTTP
```
