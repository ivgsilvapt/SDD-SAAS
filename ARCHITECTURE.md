# ARCHITECTURE.md

Este documento é a **Constitution** deste SaaS. Deve ser fornecido à IA no início de cada sessão de vibe coding.

**Arquivos complementares do kit:**
- `AGENTS.md` — prompts dos agentes e fluxo SDD
- `SPEC_TEMPLATE.md` — formato obrigatório dos SPECs
- `TESTING_GUIDE.md` — estratégia de testes por camada
- `SAAS_PATTERNS.md` — padrões específicos para SaaS (multi-tenancy, billing, GDPR)
- `GLOSSARY_TEMPLATE.md` — template de Ubiquitous Language por bounded context
- `STATE_TEMPLATE.md` — memória persistente do projeto (decisões, bloqueios, ideias adiadas)
- `PROJECT_TEMPLATE.md` — visão de produto e propósito do SaaS
- `ROADMAP_TEMPLATE.md` — roadmap de features e milestones

---

## 0. INÍCIO DE SESSÃO — LEIA ANTES DE GERAR QUALQUER CÓDIGO

Você está trabalhando em um SaaS com arquitetura **MVC + Clean Architecture + DDD**, desenvolvido com **SDD (Specification-Driven Development)** usando a metodologia **spec-kit**.

**Fluxo spec-kit obrigatório:**
```
Constitution (este arquivo) → Specify → Clarify → Checklist → Plan → Tasks (SPRINTs) → Analyze → Implement → Test
```

**Regra SDD — obrigatória:** Toda funcionalidade nova exige um SPEC aprovado em `specs/[dominio]/[feature].md` antes de qualquer implementação. Se receber uma descrição em linguagem natural sem SPEC correspondente, não implemente — informe ao usuário e use `/new-spec` para criar o SPEC primeiro.

**Referências SDD:**
- Formato de SPECs → `SPEC_TEMPLATE.md`
- Fluxo de agentes → `AGENTS.md`
- Skills disponíveis → `/new-spec`, `/impl-sprint`, `/review-arch`, `/new-domain`, `/test-sprint`

**Antes de escrever qualquer código, responda internamente estas perguntas:**

1. Existe um SPEC aprovado para esta funcionalidade? Se não, pare e crie um.
2. Em qual SPRINT do SPEC este código pertence?
3. Em qual camada este código pertence? (presentation / application / domain / infrastructure)
4. Qual bounded context está sendo trabalhado?
5. O domínio já foi modelado? Se não, modele-o antes de qualquer outra camada.
6. As interfaces de repositório necessárias já existem no domínio?
7. Existe um Command Object em `presentation/input/` para validar os dados de entrada?
8. Há strings visíveis ao usuário que precisam de chave i18n?
9. A lógica transversal (logging, auditoria, segurança) vai para middleware — não para o domínio.
10. Este SPEC envolve múltiplos tenants? Se sim, consulte `SAAS_PATTERNS.md` antes de modelar o domínio.
11. Quais testes são necessários para este SPRINT? Consulte `TESTING_GUIDE.md`.
12. Para cada biblioteca externa usada neste SPRINT: existe exemplo de uso no codebase? Se não, qual é a versão exata em uso (veja `.specs/codebase/STACK.md` se disponível)? Siga o Protocolo de Verificação de Conhecimento do `AGENTS.md` antes de implementar.

Se não conseguir responder todas, pergunte ao usuário antes de gerar código.

**Antes de criar qualquer arquivo novo (interface, entidade, value object, repositório):** pesquise se já existe usando Glob ou Grep. Nunca crie duplicata de interface de repositório, entidade de domínio ou value object — duplicatas introduzem inconsistência silenciosa e são difíceis de detectar em revisão.

---

## 1. Regras Imperativas

### 1.1 Regras Críticas — nunca viole

**Separação de camadas**
- Nunca importe classes de infraestrutura (ORM, HTTP client, banco) dentro do domínio ou dos use cases.
- Nunca coloque lógica de negócio no Controller, na View ou no ViewModel.
- Nunca acesse a camada de infraestrutura diretamente a partir da presentation — sempre passe pelo use case.
- Nunca compartilhe entidades de domínio entre bounded contexts — use eventos de domínio para comunicação entre eles.
- Nunca acesse objetos internos de um Aggregate diretamente — sempre passe pelo Aggregate Root.

**Dependências e instanciação**
- Nunca instancie dependências externas com `new` dentro de serviços, use cases ou domínio — receba-as via injeção de dependência.
- Nunca dependa de implementações concretas — dependa de interfaces definidas no domínio.

**Transações**
- Abra e feche transações de banco de dados apenas na camada de Application (Use Cases). Nunca no Controller, nunca no Domínio.

**Configuração**
- Nunca coloque valores de configuração hardcoded no código — use variáveis de ambiente.
- Nunca armazene estado entre requisições em variáveis de processo.

**Erros**
- Nunca retorne `null` silenciosamente em erros — use `Result<T, E>` ou lance exceção tipada.
- Nunca silencie exceções com bloco catch vazio ou log sem propagação.
- Nunca exponha stack traces ou detalhes internos ao cliente — mapeie para error codes seguros.

**i18n**
- Nunca coloque texto literal visível ao usuário em views — use sempre uma chave de tradução.
- Todo error code de AppError deve ter uma chave i18n correspondente.

**Multi-tenancy**
- Nunca acesse dados sem filtrar por TenantId quando o domínio é multi-tenant.
- Nunca passe TenantId como parâmetro de método — injete via TenantContext.
- Nunca armazene TenantId em variável global ou singleton — use escopo de requisição.

**Segurança**
- Nunca confie em dados de entrada sem validação — valide no Command Object (Fail Fast na borda).
- Nunca autorize uma operação sem verificar se o tenant/usuário tem permissão para o recurso específico.
- Nunca concatene input do usuário em queries — use parâmetros ou ORM.

**Escopo da tarefa**
- Nunca implemente funcionalidades além do que foi solicitado na tarefa atual.

---

### 1.2 Boas Práticas — siga sempre que possível

**Design de código**
- Mantenha cada classe, módulo e função com uma única responsabilidade. Se uma classe tem mais de uma razão para mudar, extraia.
- Estenda comportamentos via novas classes ou estratégias — evite modificar código existente para adicionar funcionalidade.
- Quando precisar adicionar comportamento, prefira composição a herança.
- Mantenha interfaces pequenas e focadas — nenhum implementador deve ser forçado a implementar métodos que não usa.
- Separe métodos de leitura de métodos de escrita — um método não deve ao mesmo tempo ler e modificar estado.
- Evite encadeamentos de chamadas profundos (`a.b().c().d()`) — o objeto deve expor o que o chamador precisa.
- Cada regra de negócio deve existir em um único lugar. Duplique estrutura se necessário, nunca conhecimento.

**Preocupações transversais**
- Aplique logging, auditoria, cache e segurança via middleware ou interceptadores — nunca inline em lógica de negócio.
- Se a mesma lógica técnica aparece em múltiplos lugares, ela pertence a um aspecto, não ao domínio.

**Framework e convenções**
- Siga as convenções do framework — adicione configuração apenas para o que é exceção à convenção.
- Nomes de arquivos, rotas e estrutura de pastas devem seguir o padrão do framework sem configuração extra.

**Serviços externos**
- Banco de dados, e-mail, storage e filas são recursos plugáveis — acesse-os sempre via interface, nunca diretamente.
- Envolva chamadas a serviços externos com timeout e política de retry — nunca faça chamadas sem proteção de falha.

**Testes**
- Escreva testes que validem comportamento, não implementação interna.
- Mocke apenas nas fronteiras da arquitetura (interfaces de repositório, serviços externos) — nunca dentro do domínio.
- Cada cenário Given-When-Then do SPEC deve ter pelo menos um teste correspondente.

**Performance e dados**
- Use read models separados (CQRS) para relatórios e dashboards — não reutilize repositórios de escrita para queries pesadas.
- Evite o problema N+1: carregue associações necessárias em uma única query quando possível.
- Aplique cache nos read models — nunca nas entidades de domínio.

---

## 2. Estrutura de Pastas

```
src/
├── presentation/               # Camada MVC — apresentação apenas
│   ├── controllers/            # Recebe requisição, chama Use Case, retorna ViewModel
│   ├── views/                  # Templates — apenas chaves i18n, sem texto literal
│   ├── viewmodels/             # Dados formatados para a view (não são entidades de domínio)
│   ├── input/                  # Command Objects — validação e binding de dados da requisição
│   └── middleware/             # Auth, i18n, rate limit, logging, TenantContext (AOP)
│
├── application/                # Casos de uso — fronteira transacional
│   └── [dominio]/
│       ├── commands/           # Operações que modificam estado
│       ├── queries/            # Operações que leem estado (podem ter read models próprios)
│       └── jobs/               # Job Use Cases — processamento assíncrono (ver Seção 19)
│
├── domain/                     # Núcleo do negócio — zero dependências externas
│   └── [dominio]/
│       ├── entities/           # Objetos com identidade e ciclo de vida
│       ├── value-objects/      # Objetos imutáveis definidos por seus atributos
│       ├── repositories/       # Interfaces de acesso a dados (sem implementação)
│       ├── events/             # Eventos de domínio (ex: PaymentFailed, UserCreated)
│       └── services/           # Lógica que não pertence a uma entidade específica
│
├── infrastructure/             # Implementações concretas das interfaces do domínio
│   ├── database/
│   │   ├── repositories/       # Implementa interfaces de domain/[dominio]/repositories/
│   │   └── migrations/         # Scripts forward-only de schema (com timestamp no nome)
│   ├── workers/                # Scheduler e runners de background jobs (ver Seção 19)
│   ├── mail/
│   ├── storage/
│   └── payment/
│
├── shared/                     # Código verdadeiramente transversal
│   ├── i18n/                   # Configuração e arquivos de tradução
│   ├── errors/                 # Result<T,E>, AppError base, hierarquia de erros, error codes
│   ├── tenant/                 # TenantContext — propagação do tenant pela requisição
│   └── container/              # Configuração do container de DI / IoC
│
├── config/                     # Variáveis de ambiente e configuração (sem lógica)
│
└── tests/                      # Todos os testes — espelham a estrutura de src/
    ├── unit/
    │   ├── domain/             # Entidades, value objects, serviços de domínio
    │   └── application/        # Use cases com repositórios em memória
    ├── integration/
    │   ├── infrastructure/     # Repositórios reais contra banco de teste
    │   └── presentation/       # Controllers com test client HTTP
    └── e2e/                    # Fluxos de negócio completos
```

---

## 3. Fluxo de Desenvolvimento (Domain-First)

Desenvolva sempre de dentro para fora. Nunca comece pela UI ou pelo banco de dados.

> **API-First vs Domain-First:** Não são conflitantes — atuam em fases diferentes. **API-First** (Seção 17) refere-se ao *design*: o contrato de API é definido no SPEC antes de qualquer código. **Domain-First** é a *ordem de implementação*: mesmo com o contrato definido, o código começa sempre pelo domínio.

```
1. DOMÍNIO
   └── Entidades, value objects e eventos do bounded context
   └── Interfaces de repositório necessárias
   └── [RED]      Escreva o teste unitário para o cenário GWT (deve falhar)
   └── [GREEN]    Implemente o mínimo para o teste passar
   └── [REFACTOR] Limpe o código sem quebrar o teste — repita por cenário GWT

2. APPLICATION
   └── Use Cases (Commands e Queries)
   └── Fronteira transacional configurada
   └── [RED]      Escreva o teste do use case com InMemoryRepository (deve falhar)
   └── [GREEN]    Implemente a orquestração mínima para o teste passar
   └── [REFACTOR] Limpe o código sem quebrar o teste — repita por cenário GWT

3. INFRAESTRUTURA
   └── Implementações das interfaces de repositório
   └── Migrations de banco de dados (forward-only)
   └── Integrações externas (mail, storage, pagamento)
   └── Testes de integração gerados pelo Agente Testing após implementação
        (TDD completo aqui é opcional — setup de banco real dificulta o ciclo)

4. APRESENTAÇÃO
   └── Command Object de validação (presentation/input/)
   └── Controller
   └── ViewModel
   └── View com chaves i18n
   └── Testes de integração gerados pelo Agente Testing após implementação
        (TDD completo aqui é opcional — setup de HTTP client dificulta o ciclo)

5. ASPECTOS TRANSVERSAIS
   └── Middleware de logging, auditoria ou segurança (se necessário)
   └── Testes e2e: fluxos críticos do início ao fim
```

Se não conseguir modelar o domínio de uma funcionalidade, não gere código — discuta o modelo antes.

---

## 4. Fluxo de uma Requisição

```
Requisição HTTP
     │
     ▼
Middleware                         ← auth (JWT), i18n, rate limit, logging, TenantContext (AOP)
     │                               Correlation ID gerado aqui e propagado em todos os logs
     ▼
Controller                         ← recebe Request, retorna Response
     │  instancia Command Object (presentation/input/)
     │  valida entrada — lança erro imediatamente se inválida (Fail Fast)
     │  verifica autorização RBAC
     │  passa Command ou Query ao Use Case
     ▼
Use Case                           ← orquestra e gerencia a transação
     │  recebe TenantContext e User via DI
     ▼
Domain (Entities, Services)        ← executa regras de negócio puras
     │  retorna Result<T, E> — nunca null
     ▼
Repository Interface               ← domínio chama a interface (nunca a implementação)
     │
     ▼
Repository Implementation          ← infraestrutura persiste no banco (filtra por TenantId)
     │
     ▼
Resultado retorna pelas camadas
     │
     ▼
Controller monta ViewModel         ← nunca expõe entidades de domínio diretamente
     │  mapeia error codes para HTTP status
     ▼
View renderiza com chaves i18n
     │
     ▼
Resposta HTTP (com Correlation-Id no header)
```

---

## 5. Checklist de Revisão

Aplique este checklist em todo código gerado antes de aceitar.

**Camadas e arquitetura**
- [ ] O código está na camada correta?
- [ ] O domínio foi modelado antes das outras camadas?
- [ ] O domínio importa algo de infraestrutura?
- [ ] A transação está sendo aberta fora do Use Case?
- [ ] Preocupações transversais (log, segurança) estão no middleware?

**SOLID**
- [ ] A classe tem mais de uma razão para mudar? (SRP)
- [ ] A mudança exigiu modificar código existente em vez de estender? (OCP)
- [ ] Alguma interface tem métodos que o implementador não usa? (ISP)
- [ ] Alguma dependência foi instanciada com `new` em vez de injetada? (DIP)

**Design de código**
- [ ] Algum método lê e modifica estado ao mesmo tempo? (CQS)
- [ ] Existe regra de negócio duplicada em mais de um lugar? (DRY)
- [ ] Existe encadeamento profundo como `a.b().c().d()`? (Law of Demeter)
- [ ] Foi usada herança onde composição resolveria? (Composition over Inheritance)
- [ ] Algum erro é silenciado, retornado como `null`, ou sem error code? (Fail Fast)
- [ ] Foi gerado algo além do que foi solicitado? (YAGNI)

**Desacoplamento**
- [ ] Existe Command Object para validação de entrada?
- [ ] Serviços externos são acessados via interface?
- [ ] Foi adicionada configuração onde convenção do framework resolve? (CoC)

**12-Factor**
- [ ] Algum valor de configuração está hardcoded?
- [ ] O código armazena estado entre requisições?

**DDD**
- [ ] A nomenclatura usa a Ubiquitous Language do domínio?
- [ ] Entidades de domínio são compartilhadas entre bounded contexts?
- [ ] Objetos internos de Aggregate são acessados sem passar pelo Aggregate Root?

**Multi-tenancy**
- [ ] Todo acesso a dados filtra por TenantId?
- [ ] TenantId é injetado via TenantContext — não lido de variável global?

**Segurança**
- [ ] Input do usuário é validado antes de qualquer processamento?
- [ ] O controller verifica autorização antes de chamar o use case?
- [ ] Stack traces ou dados sensíveis são expostos ao cliente?
- [ ] Queries usam parâmetros (não concatenação de strings)?

**Erros**
- [ ] Erros de negócio retornam Result<T, E> com error code?
- [ ] Error codes têm chave i18n correspondente?
- [ ] InfrastructureErrors são logados internamente e mapeados para código genérico ao cliente?

**Testes**
- [ ] Cada cenário Given-When-Then do SPEC tem pelo menos um teste?
- [ ] Os testes mocam apenas nas fronteiras da arquitetura?
- [ ] O teste valida comportamento, não implementação interna?

**i18n**
- [ ] Existe string visível ao usuário sem chave i18n?

---

## REFERÊNCIA

As seções abaixo são material de referência. Use-as para entender decisões arquiteturais e padrões — não como guia de ação direta.

---

## 6. Arquitetura em Camadas

MVC como padrão de **apresentação**, Clean Architecture como **estrutura de aplicação**. O Model do MVC é sempre um ViewModel — nunca contém lógica de negócio.

```
┌─────────────────────────────────────────────────┐
│                  PRESENTATION                    │
│         View  ←→  Controller  ←→  ViewModel     │  ← MVC (apresentação apenas)
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│                  APPLICATION                     │
│            Use Cases  /  Commands  /  Queries    │  ← Orquestra e gerencia transações
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│                    DOMAIN                        │
│       Entities  /  Value Objects  /  Events      │  ← Regras de negócio puras
│       Repository Interfaces  /  Domain Services  │  ← Zero dependências externas
└────────────────────────┬────────────────────────┘
                         │
┌────────────────────────▼────────────────────────┐
│                INFRASTRUCTURE                    │
│    Database  /  Mail  /  Storage  /  Gateways    │  ← Implementações concretas
└─────────────────────────────────────────────────┘
```

A seta de dependência aponta sempre para dentro. Camadas internas nunca importam camadas externas.

---

## 7. Domain-Driven Design (DDD)

### Ubiquitous Language
O código usa os mesmos termos que o negócio usa.

```
// Errado
UserPlan, ClientRecord, Bill, SystemUser

// Correto
Subscription, Tenant, Invoice, Account
```

### Bounded Contexts
Cada domínio tem seus próprios modelos isolados. O `User` de Autenticação é diferente do `User` de Billing. Contextos se comunicam via eventos de domínio — nunca compartilhando entidades.

> **DRY dentro e entre BCs:** O DRY aplica-se *dentro* de um Bounded Context — conhecimento de negócio não se repete dentro do mesmo BC. *Entre* BCs, duplicação de implementação é aceitável se os modelos representam conceitos genuinamente separados (ex: validação de e-mail em Auth e em Billing podem ter regras distintas). Compartilhar código entre BCs via `shared/` é permitido apenas para utilitários técnicos puros (ex: `Result<T>`, formatadores) — nunca para regras de negócio.

### Aggregates
Grupos de entidades que mudam juntos possuem um único ponto de entrada (Aggregate Root). Objetos internos são sempre acessados pela raiz.

### Domain Events — Síncronos vs Assíncronos

Eventos de domínio têm dois papéis com mecanismos diferentes:

| Escopo | Tipo | Quando disparar | Como implementar |
|---|---|---|---|
| Dentro do mesmo BC | **Síncrono** | No Use Case, antes do commit da transação | Dispatch direto pelo repositório ou event bus local |
| Entre BCs diferentes | **Assíncrono** | Via Outbox — persistido na mesma transação do domínio, publicado por worker | Outbox pattern (ver Seção 19) |

**Regra:** Nunca dispare um evento assíncrono diretamente dentro do Use Case sem o Outbox — se o processo crasha após o commit e antes da publicação, o evento se perde permanentemente.

### Unit of Work — Controle de Transação na Application Layer

A regra "abra e feche transações apenas no Use Case" (Seção 1.1) é implementada via **Unit of Work**:

```
// Interface definida no domínio (sem importar infraestrutura)
interface IUnitOfWork {
  begin(): Promise<void>
  commit(): Promise<void>
  rollback(): Promise<void>
}

// Use Case recebe UoW via DI e coordena a transação
class CreateInvoiceUseCase {
  constructor(
    private readonly invoiceRepo: IInvoiceRepository,
    private readonly subscriptionRepo: ISubscriptionRepository,
    private readonly uow: IUnitOfWork
  ) {}

  async execute(command: CreateInvoiceCommand): Promise<Result<Invoice>> {
    await this.uow.begin()
    try {
      // ... lógica de negócio usando ambos os repositórios
      await this.uow.commit()
    } catch (e) {
      await this.uow.rollback()
      throw e
    }
  }
}
```

**Regras:**
- `IUnitOfWork` é definida no domínio ou em `shared/` — nunca na infraestrutura
- A implementação concreta (`DatabaseUnitOfWork`) fica na infraestrutura e gerencia a transação real
- Use UoW apenas quando dois ou mais repositórios precisam ser atômicos — não envolva operações independentes

### CQRS — Read Models Separados
Para queries complexas (relatórios, dashboards, listagens com joins), use read models separados:
- **Commands** usam repositórios de escrita: domain → interface → infra
- **Queries pesadas** usam read models otimizados em `application/[dominio]/queries/`
- Read models são DTOs de leitura — não são entidades de domínio
- Read models podem ler diretamente de views de banco ou tabelas desnormalizadas

**Regra de decisão — quando usar read model vs repositório de escrita:**

| Use repositório de escrita quando... | Use read model quando... |
|---|---|
| Buscar por `id` ou campo único para operar sobre a entidade | A query envolve JOIN entre múltiplas tabelas ou aggregates |
| O resultado será modificado e persistido | A query é para exibição (listagem, relatório, dashboard) |
| A operação é dentro de um Use Case de comando | A query usa agregações (COUNT, SUM, GROUP BY) |
| — | O resultado combina dados de múltiplos bounded contexts |

> **Regra simples:** Se você vai modificar o resultado, use repositório. Se vai apenas exibir, use read model.

---

## 8. Tratamento de Erros

### Padrão Result\<T, E\>
Use Result para erros esperados do negócio. Lance exceções apenas para falhas inesperadas (infra, bugs).

```
// Estrutura mínima
Result<TValue>
  .ok(value)      → sucesso com valor
  .fail(error)    → falha com AppError tipado

// Uso no Use Case
const result = subscriptionService.cancel(subscriptionId)
if (result.isFail()) return result  // propaga o erro

// Uso no Controller
if (result.isFail()) {
  return Response(
    status: errorCodeToHttpStatus(result.error.code),
    body: { code: result.error.code, messageKey: result.error.messageKey }
  )
}
```

### Hierarquia de Erros

```
AppError (base — code: string, messageKey: string)
├── DomainError           ← violação de regra de negócio → HTTP 400/422
│   ├── ValidationError   ← campo inválido
│   └── BusinessRuleViolation ← estado inválido para a operação
├── NotFoundError         ← recurso inexistente → HTTP 404
├── AuthorizationError    ← sem permissão → HTTP 403
├── ConflictError         ← conflito de estado → HTTP 409
└── InfrastructureError   ← falha de sistema → HTTP 500 (nunca expor detalhes ao cliente)
```

### Error Codes
Strings estáticas em SCREAMING_SNAKE_CASE, prefixadas pelo domínio:
```
SUBSCRIPTION_ALREADY_CANCELED
PAYMENT_METHOD_EXPIRED
TENANT_NOT_FOUND
INVOICE_ALREADY_PAID
```

Regras:
- Cada error code tem uma chave i18n correspondente no locale do domínio
- InfrastructureErrors são logados internamente com stack trace; o cliente recebe apenas `INTERNAL_ERROR`
- Nunca exponha nomes de tabela, colunas ou mensagens do ORM ao cliente

---

## 9. Design de API

### Versionamento
- Versione na URL: `/api/v1/[recurso]`
- Adicionar campo é backward compatible — não requer nova versão
- Remover ou alterar campo é breaking — requer nova versão
- Mantenha a versão anterior disponível por pelo menos 1 ciclo de release após deprecação

### Convenções REST

| Operação | Método | Rota exemplo | Status |
|---|---|---|---|
| Listar | GET | `/api/v1/invoices` | 200 |
| Detalhar | GET | `/api/v1/invoices/:id` | 200 / 404 |
| Criar | POST | `/api/v1/invoices` | 201 |
| Atualizar (parcial) | PATCH | `/api/v1/invoices/:id` | 200 |
| Substituir | PUT | `/api/v1/invoices/:id` | 200 |
| Remover | DELETE | `/api/v1/invoices/:id` | 204 |

### Paginação (cursor-based preferido)
```json
{
  "data": [...],
  "meta": { "nextCursor": "eyJpZCI6MTAwfQ==", "hasMore": true }
}
```

### Filtros e Ordenação
```
GET /api/v1/invoices?status=paid&sort=-createdAt&limit=25
```

### Idempotência
Para POST com efeito colateral (pagamento, envio de e-mail):
- Suporte o header `Idempotency-Key`
- Armazene o resultado da 1ª execução por chave (TTL: 24h)
- Retorne o mesmo resultado para chaves repetidas sem reprocessar

### Envelope de Resposta

```json
// Sucesso simples
{ "data": { "id": "...", ... } }

// Lista
{ "data": [...], "meta": { "nextCursor": "...", "hasMore": true } }

// Erro
{ "error": { "code": "SUBSCRIPTION_ALREADY_CANCELED", "messageKey": "subscription.error.alreadyCanceled" } }
```

---

## 10. Observabilidade

### Os Três Pilares
- **Logs** — o que aconteceu e em qual contexto
- **Métricas** — frequência, latência, taxa de erro (dados quantitativos)
- **Traces** — onde o tempo foi gasto em flows distribuídos

### Health Checks

Todo serviço deve expor dois endpoints de saúde (sem autenticação, sem TenantContext):

| Endpoint | Nome | O que verifica | Quando retorna 503 |
|---|---|---|---|
| `GET /health/live` | Liveness | Processo está vivo | Nunca (se responder, está vivo) |
| `GET /health/ready` | Readiness | Banco conectado, migrations aplicadas, dependências críticas up | Qualquer dependência crítica indisponível |

```json
// Resposta padrão de /health/ready (200 OK)
{
  "status": "ok",
  "checks": {
    "database": "ok",
    "migrations": "ok"
  }
}

// Resposta de /health/ready quando degradado (503)
{
  "status": "degraded",
  "checks": {
    "database": "error: connection timeout",
    "migrations": "ok"
  }
}
```

**Regras:**
- Health checks nunca expõem stack traces ou detalhes de infra — apenas `ok` / `error`
- Liveness usado por container orchestrators (K8s, ECS) para restart automático
- Readiness usado para remover instância do load balancer sem reiniciá-la
- Nunca inclua checks de dependências não-críticas (ex: serviço de e-mail) no readiness — use health separado se necessário

### Correlation ID
- Gerado no middleware de entrada (UUID v4)
- Propagado via header: `X-Correlation-Id`
- Incluído em **todos** os logs da requisição
- Retornado no header da resposta para rastreabilidade pelo cliente

### Logging Estruturado
```json
{
  "timestamp": "2025-01-15T10:30:00.000Z",
  "level": "INFO",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "tenantId": "tenant-uuid",
  "userId": "user-uuid",
  "event": "subscription.canceled",
  "durationMs": 45
}
```

Níveis:
- **ERROR** — falha que requer ação humana (sempre com stack trace interno, nunca exposto)
- **WARN** — degradação ou comportamento inesperado recuperável
- **INFO** — eventos de negócio relevantes (criação, cancelamento, pagamento)
- **DEBUG** — diagnóstico técnico (apenas em dev/staging)

Regras:
- Nunca logue senhas, tokens, números de cartão ou PII sem mascaramento
- Escreva em stdout — nunca gerencie arquivos de log na aplicação (12-Factor)
- Stack traces apenas nos logs internos — nunca na resposta ao cliente

---

## 11. Segurança

### Fluxo de Autenticação e Autorização
```
Request → Middleware Auth → valida JWT → extrai User + TenantId → injeta TenantContext
                         → retorna 401 se token inválido ou expirado

Controller → verifica permissão RBAC para a operação → retorna 403 se não autorizado
Use Case   → opera apenas dentro do TenantContext injetado — nunca lê dados de outros tenants
```

- JWT validado **no middleware** — nunca no controller ou use case
- RBAC resolvido no controller (ou serviço de autorização injetado via DI)
- Use cases recebem o usuário autenticado via DI — nunca releem o token

### Defense in Depth
Valide em múltiplas camadas — uma não substitui a outra:

| Camada | Validação |
|---|---|
| Presentation (Command Object) | Formato, tipos, campos obrigatórios |
| Application (Use Case) | Regras de negócio, ownership, status do recurso |
| Infrastructure (Repository) | TenantId em toda query (row-level security) |

### OWASP — Itens Críticos para SaaS

| Risco | Mitigação arquitetural |
|---|---|
| Broken Access Control | Filtrar por TenantId em toda query; verificar ownership antes de operar |
| Injection | Nunca concatenar input em queries — use parâmetros ou ORM |
| Security Misconfiguration | Secrets via variáveis de ambiente; nunca hardcode |
| Sensitive Data Exposure | Nunca logar PII; HTTPS obrigatório; mascarar dados sensíveis em logs |
| Rate Limiting | Middleware por tenant e por endpoint |
| Broken Authentication | JWT com expiração curta + refresh token rotativo; invalidar no logout |
| IDOR | Verificar que o recurso pertence ao tenant/usuário antes de qualquer operação |
| CSRF | Token anti-CSRF para formulários; SameSite cookies |

### Dados Sensíveis e LGPD/GDPR
- Defina no SPEC quais campos são PII (Personally Identifiable Information)
- Implemente soft delete com flag `deletedAt` para conformidade com direito ao esquecimento
- Dados de PII são mascarados em logs e excluídos de exports não autorizados
- Retenção de dados configurável por tipo de dado

### Soft Delete — Comportamento do Repositório

Quando o domínio usa soft delete (`deletedAt`), o comportamento dos repositórios deve ser explícito:

| Método | Comportamento padrão |
|---|---|
| `findById(id)` | Retorna `NotFoundError` se `deletedAt IS NOT NULL` |
| `findAll(filter)` | Filtra automaticamente `WHERE deletedAt IS NULL` |
| `findByIdIncludeDeleted(id)` | Retorna mesmo que deletado — para uso em auditoria |
| `delete(id)` | Seta `deletedAt = now()` — nunca executa `DELETE` físico |

**Regras:**
- O filtro `deletedAt IS NULL` é responsabilidade do repositório, não do Use Case — o domínio não deve conhecer esse detalhe de persistência
- Métodos `includeDeleted` são explicitamente nomeados — nunca silenciosos
- Hard delete físico é permitido apenas em fluxos de conformidade LGPD (direito ao esquecimento), via Use Case específico com log de auditoria

---

## 12. Resiliência

Aplique em toda chamada a serviços externos (banco, APIs, filas, storage):

### Timeout
- Defina timeout explícito em toda chamada externa
- Padrões recomendados: banco 5s, APIs 10s, storage 30s, filas 15s
- Timeout configurável via variável de ambiente

### Retry com Backoff Exponencial
```
Tentativa 1: imediata
Tentativa 2: após 1s
Tentativa 3: após 2s
Tentativa 4: após 4s
Máximo: 3 retentativas — apenas para erros recuperáveis (5xx, timeout, rede)
Sem retry: erros 4xx (client error) — não tente novamente
```

### Circuit Breaker
Para integrações críticas (gateway de pagamento, e-mail, serviços externos):
- **Closed** — operação normal, chamadas passam
- **Open** — N falhas consecutivas detectadas → bloqueia chamadas, retorna erro imediato por T segundos
- **Half-Open** — após T segundos, testa 1 chamada; se ok volta a Closed, se falhar volta a Open

### Regra geral
Toda interface de serviço externo declara sua política de resiliência. O Use Case não implementa retry — a camada de infraestrutura implementa.

---

## 13. Migrations

1. **Forward-only** — nunca escreva migration de rollback automático; rollback é sempre uma nova migration
2. **Uma responsabilidade por migration** — não misture DDL com seed de dados
3. **Compatível com a versão anterior do código** — pode ser executada antes do deploy sem quebrar o sistema atual
4. **Nunca altere uma migration já executada em produção** — crie uma nova
5. **Nomenclatura com timestamp**:
   ```
   20250115_143022_create_subscriptions_table.sql
   20250118_091500_add_paused_status_to_subscriptions.sql
   ```
6. **Nunca valores hardcoded sensíveis em migrations** — use variáveis de ambiente para seeds
7. **Teste de integração obrigatório** para migrations que alteram tabelas existentes (antes e depois)

---

## 14. Estratégia de Testes

> Guia completo em `TESTING_GUIDE.md`. Esta seção é o resumo operacional.

### Pirâmide de Testes

```
         /\
        /  \
       / E2E \        ← Poucos: happy path + fluxos críticos de negócio
      /--------\
     /Integration\    ← Médio: repositórios reais, controllers, serviços externos
    /------------\
   /  Unit Tests  \   ← Maioria: entidades, value objects, use cases (repos em memória)
  /________________\
```

### O que testar por camada

| Camada | Tipo | O que testar |
|---|---|---|
| Domain | Unit | Invariantes de entidade, validações de value object, transições de estado, regras de negócio |
| Application | Unit | Orquestração do use case (com InMemoryRepository), resultado esperado por cenário |
| Infrastructure | Integration | Queries reais contra banco de teste, mapeamento ORM, repositórios concretos |
| Presentation | Integration | Endpoints: status code, corpo da resposta, autenticação, validação de input |
| E2E | E2E | Fluxos de negócio completos do início ao fim |

### Regra de mapeamento SPEC → Teste
Cada cenário Given-When-Then do SPEC corresponde a pelo menos 1 teste:
- **Given** → setup do teste (arrange)
- **When** → ação executada (act)
- **Then** → assertion sobre o resultado (assert)

---

## 15. Padrões SaaS

> Guia completo em `SAAS_PATTERNS.md`. Esta seção é o resumo operacional.

### Multi-tenancy
- Estratégia padrão: **row-level isolation** — todos os tenants no mesmo banco, filtrados por `tenantId`
- TenantId é extraído do JWT no middleware e injetado no TenantContext (escopo de requisição)
- Todos os repositórios recebem TenantContext via DI e incluem `WHERE tenantId = :tenantId` em toda query
- Nunca passe `tenantId` como parâmetro de método — injete via contexto

### TenantContext — Fluxo de Propagação
```
Middleware extrai tenantId do JWT
  → injeta TenantContext no container de DI (escopo da requisição)
  → Use Cases recebem TenantContext via construtor
  → Repositórios recebem TenantContext via construtor
  → Toda query inclui WHERE tenantId = :tenantId
```

### Feature Flags
- Interface no domínio: `IFeatureFlagService`
- Implementação na infraestrutura (banco de dados, serviço externo)
- Use para: rollout gradual, beta features por tenant, features por plano de preço

---

## 16. Otimização de Contexto para AI (Token Efficiency)

Para minimizar custo de tokens ao usar AI agents, forneça apenas o contexto necessário por agente:

| Agente | Contexto mínimo necessário |
|---|---|
| **Spec** | `ARCHITECTURE.md` seções 0–3 + `SPEC_TEMPLATE.md` + `GLOSSARY_TEMPLATE.md` do projeto + descrição da feature |
| **Analyze** | SPEC completo + `ARCHITECTURE.md` seções 1 e 5 |
| **Implementation Sprint 1** | `ARCHITECTURE.md` seções 0–5 + SPRINT 1 do SPEC |
| **Implementation Sprint 2+** | `ARCHITECTURE.md` seções 0–5 + SPRINT N do SPEC + interfaces de repositório do domínio existentes |
| **Review** | Código gerado do SPRINT + seção do SPRINT (com GWT) + `ARCHITECTURE.md` seções 1 e 5 |
| **Testing** | Código gerado do SPRINT + cenários GWT do SPRINT + `TESTING_GUIDE.md` |
| **Migration** | Entidades do SPRINT 1 + schema atual do banco + `ARCHITECTURE.md` seção 13 |

**Regras de ouro:**
- Nunca forneça a codebase inteira para um agente — forneça apenas os arquivos do SPRINT atual
- SPRINTs com mais de 5 FRs ou 6+ arquivos novos devem ser divididos em sub-SPRINTs (1a, 1b...)
- Execute o Checklist de Cobertura do SPEC antes de pedir implementação — evita regeneração custosa
- Aprovação humana do SPEC antes do Analyze elimina ciclos de correção desnecessários

**Ordem correta de carregamento de contexto (do mais para o menos prioritário):**
1. `ARCHITECTURE.md` seções relevantes — as restrições devem ser carregadas primeiro
2. `STATE.md` — decisões acumuladas do projeto
3. SPEC/SPRINT específico — o contrato de comportamento a implementar
4. Interfaces e entidades existentes — referências do código já criado

**Sinais de alerta de contexto excessivo:**

Se qualquer sinal abaixo aparecer durante uma sessão, **pause com `/pause-session`** e reinicie com contexto mínimo:

| Sinal | Provável causa | Ação |
|---|---|---|
| Agente responde de forma genérica, sem citar o SPEC | Contexto muito grande, SPEC perdido no meio | `/pause-session` → reinicie com SPEC + ARCHITECTURE.md seções 0–5 |
| Agente confunde FRs de SPRINTs diferentes | SPEC inteiro carregado quando só um SPRINT era necessário | Forneça apenas a seção do SPRINT atual |
| Agente "esquece" regra que citou no início da sessão | Janela de contexto esgotando | `/pause-session` imediatamente |
| Agente propõe padrão já descartado (registrado no STATE.md) | STATE.md não foi carregado | Reinicie incluindo `@STATE.md` |

**Divisão em sub-SPRINTs (para SPRINTs grandes):**

Quando um SPRINT tem mais de 5 FRs ou vai criar mais de 6 arquivos novos:
1. Divida em `SPRINT Na` (FRs 001–003) e `SPRINT Nb` (FRs 004+)
2. Implemente e revise Na antes de iniciar Nb
3. Cada sub-SPRINT gera seu próprio commit: `feat(scope): [descrição] [spec] - sprint Na`
4. Ao concluir todos os sub-SPRINTs de um SPRINT, faça um commit de merge: `feat(scope): completa SPRINT N [spec]`

---

## 17. Princípios de Referência

> **Quando princípios colidem, use esta hierarquia de desempate:**
> 1. **Segurança e isolamento de dados** (Defense in Depth, Least Privilege, TenantId) — nunca sacrificados
> 2. **Fail Fast** — erros sinalizados imediatamente, sempre
> 3. **YAGNI > OCP** — não crie extensibilidade sem requisito conhecido; quando houver requisito, então estenda sem modificar
> 4. **Isolamento de Bounded Context > DRY** — entre BCs, duplicar implementação é preferível a acoplar contextos
> 5. **KISS** — se duas soluções atendem ao requisito, a mais simples vence

| Princípio | Regra |
|---|---|
| **SRP** | Uma razão para mudar por classe |
| **OCP** | Estenda, não modifique |
| **LSP** | Subtipos substituem o pai sem quebrar o sistema |
| **ISP** | Interfaces pequenas e focadas |
| **DIP** | Dependa de abstrações |
| **IoC** | O framework gerencia o ciclo de vida das dependências |
| **DI** | Dependências recebidas de fora, nunca criadas internamente |
| **DRY** | Conhecimento de negócio em um único lugar |
| **KISS** | A solução mais simples que resolve o problema |
| **YAGNI** | Só o que é necessário agora |
| **SoC** | Camadas separadas por responsabilidade |
| **CQS** | Leitura e escrita em métodos separados |
| **CQRS** | Read models separados para queries pesadas |
| **CoC** | Convenção primeiro, configuração só para exceções |
| **AOP** | Preocupações transversais via aspectos centralizados |
| **Fail Fast** | Erros sinalizados imediatamente na borda do sistema |
| **Law of Demeter** | Fale apenas com vizinhos imediatos |
| **Composition > Inheritance** | Componha comportamentos em vez de criar hierarquias |
| **Defense in Depth** | Segurança validada em múltiplas camadas independentes |
| **Least Privilege** | Acesso mínimo necessário por papel, tenant e operação |
| **TDD** | Red → Green → Refactor: escreva o teste antes do código de produção |
| **Testing Pyramid** | Maioria unitários, poucos e2e — testes rápidos e confiáveis |
| **API-First** | Defina o contrato de API no SPEC antes de implementar — refere-se ao *design*, não à ordem de código (que segue Domain-First) |
| **Idempotency** | Operações POST com efeito colateral suportam reenvio seguro |
| **Resilience** | Timeout + Retry + Circuit Breaker em toda integração externa |
| **Observability** | Logs + Métricas + Traces com Correlation ID em toda requisição |

### 12-Factor App (fatores relevantes)

| Fator | Regra |
|---|---|
| **Config** | Toda configuração via variáveis de ambiente |
| **Backing Services** | Serviços externos são recursos plugáveis via interface |
| **Stateless** | Estado vive no banco ou cache, nunca no processo |
| **Dev/Prod Parity** | Ambiente local espelha produção |
| **Logs** | Escreva em stdout — nunca gerencie arquivos de log |
| **Disposability** | Inicialização rápida, desligamento gracioso |
| **Port Binding** | Serviços auto-contidos — sem dependência de runtime externo |

---

## 18. Internacionalização (i18n)

### Estrutura de arquivos
```
shared/i18n/
└── locales/
    ├── pt-BR/
    │   ├── common.json       # Termos globais (botões, labels, erros genéricos)
    │   ├── auth.json
    │   ├── billing.json
    │   └── [dominio].json
    └── en/
        └── ...
```

### Convenção de chaves
Padrão: `[contexto].[elemento].[estado]` — minúsculas, separado por pontos.

```json
{
  "page.title": "Painel de Controle",
  "action.save": "Salvar",
  "error.required": "Este campo é obrigatório",
  "subscription.status.active": "Ativa",
  "subscription.error.alreadyCanceled": "Esta assinatura já foi cancelada"
}
```

### Regras
- O idioma é resolvido por middleware antes de chegar ao controller.
- O serviço de tradução é injetado via DI — a view nunca acessa arquivos diretamente.
- Um arquivo de locale por domínio — não crie um único arquivo gigante.
- Todo error code de AppError tem uma chave i18n correspondente no locale do domínio.

---

## 19. Background Jobs / Workers

SaaS tipicamente requer processamento fora do ciclo request/response: renovação de assinaturas, geração de faturas, envio de e-mails, limpeza de dados expirados.

### Onde ficam na arquitetura

```
src/
├── application/
│   └── [dominio]/
│       └── jobs/                    # Job Use Cases — mesma estrutura de commands/queries
│           ├── renew-subscriptions.job.ts
│           └── generate-monthly-invoices.job.ts
│
└── infrastructure/
    └── workers/                     # Agendamento e execução dos jobs
        ├── scheduler.ts             # Configuração de cron (ex: node-cron, Bull, BullMQ)
        └── job-runner.ts            # Instancia e executa Job Use Cases
```

### Regras

- **Job Use Cases seguem as mesmas regras dos Use Cases comuns:** recebem repositórios via DI, usam TenantContext se iteram sobre tenants, retornam `Result<T, E>`
- **Nunca coloque lógica de negócio no scheduler** — o scheduler apenas dispara; o Job Use Case executa
- **Idempotência obrigatória:** jobs devem poder ser reexecutados sem efeito duplicado (ex: fatura já gerada não é gerada novamente)
- **Tenancy em jobs:** jobs que processam múltiplos tenants iteram sobre tenants ativos e injetam um `TenantContext` por iteração — nunca processam todos sem filtro
- **Logs estruturados:** inclua `jobName`, `tenantId` (se aplicável) e `durationMs` no log de cada execução
- **Timeout e retry:** defina timeout por job; jobs com falha são retentados com backoff exponencial (máx 3x)
- **Separação de processo:** jobs intensivos (geração em massa) devem rodar em processo/worker separado para não competir com requisições HTTP

### Outbox Pattern — Entrega Confiável de Eventos entre BCs

O Outbox garante que um Domain Event entre BCs nunca se perca, mesmo que o processo crashe após o commit do banco.

**Problema sem Outbox:**
```
Use Case: commit(subscriptionCanceled) → CRASH → evento nunca publicado → BC de Billing não processa
```

**Solução com Outbox:**
```
1. Use Case persiste a entidade + o evento na tabela `outbox` na MESMA transação
2. Worker de Outbox lê eventos pendentes da tabela `outbox` e publica no message broker
3. Após confirmação de publicação, marca o evento como `processed`
```

**Estrutura da tabela `outbox`:**
```sql
CREATE TABLE outbox_events (
  id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  event_type  VARCHAR(100) NOT NULL,       -- ex: 'SubscriptionCanceled'
  payload     JSONB NOT NULL,
  tenant_id   UUID NOT NULL,
  created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
  processed_at TIMESTAMP,
  attempts    INT NOT NULL DEFAULT 0
);
```

**Regras:**
- A interface `IOutboxRepository` fica em `shared/` (usada por múltiplos BCs)
- O worker de Outbox fica em `infrastructure/workers/outbox-worker.ts`
- Eventos processados não são deletados imediatamente — mantenha por N dias para auditoria (TTL configurável)
- O worker usa `SELECT ... FOR UPDATE SKIP LOCKED` para evitar processamento duplo em múltiplas instâncias
- Eventos com mais de `MAX_ATTEMPTS` falhas são movidos para dead-letter (tabela `outbox_dead_letter`)
- O Outbox é necessário **apenas para comunicação entre BCs** — eventos dentro do mesmo BC são síncronos e não precisam de Outbox

---

## 20. Conventional Commits

Todo commit neste projeto segue o padrão **Conventional Commits 1.0.0**.

### Formato obrigatório

```
type(scope): descrição [spec-ref]
```

- **type** — categoria da mudança (tabela abaixo)
- **scope** — bounded context afetado (ex: `billing`, `auth`, `tenant`, `action-plan`)
- **descrição** — imperativo, em português, sem ponto final, máx. 72 caracteres
- **spec-ref** — slug do arquivo SPEC, entre colchetes, opcional mas recomendado

**Exemplo:**
```
feat(billing): implementa cancelamento de assinatura por inadimplência [create-subscription]
fix(auth): corrige validação de JWT expirado no middleware de tenant
test(action-plan): adiciona cobertura GWT para FR-004 e FR-005
chore(infra): cria migration 20251001_120000_add_tenant_id_to_invoices
```

### Tabela de tipos

| Tipo | Quando usar |
|---|---|
| `feat` | Nova funcionalidade proveniente de SPEC/SPRINT aprovado |
| `fix` | Correção de bug, incluindo correções via `/quick-fix` |
| `refactor` | Melhoria de código sem mudança de comportamento (ciclo REFACTOR do TDD) |
| `test` | Adição ou correção de testes (sem mudança no código de produção) |
| `docs` | Mudanças em documentação (SPECs, ARCHITECTURE.md, GLOSSARY.md) |
| `chore` | Migrations de banco, configurações, scripts de tooling |
| `ci` | Mudanças em pipelines de CI/CD |

### Regras

- **1 commit por SPRINT** aprovado (ou por FR, se o SPRINT for dividido em sub-SPRINTs)
- **Corrections via `/quick-fix`** usam sempre tipo `fix(scope):`
- **Migrations** usam `chore(infra):` com o nome do arquivo de migration na descrição
- **Nunca commite** código de um SPRINT que recebeu `REPROVADO` do Agente Review
- **O idioma** da mensagem de commit segue o idioma principal de desenvolvimento do projeto
- **O Agente Review** sugere automaticamente a mensagem de commit ao emitir veredicto `APROVADO`

### Integração com o fluxo SDD

```
SPRINT implementado + testes gerados
           │
           ▼
   Agente Review → APROVADO
           │
           ▼
   "Commit Sugerido:" feat(scope): descrição [spec-ref]
           │
           ▼
   git commit -m "feat(scope): descrição [spec-ref]"
```
