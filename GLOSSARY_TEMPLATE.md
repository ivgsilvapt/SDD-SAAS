# GLOSSARY_TEMPLATE.md

Template para documentar a **Ubiquitous Language** de cada SaaS.

**Instrução de uso:**
1. Copie este arquivo para `specs/[nome-do-projeto]/GLOSSARY.md`
2. Preencha **antes** de criar o primeiro SPEC do projeto
3. Forneça o GLOSSARY.md ao Agente Spec junto com o ARCHITECTURE.md
4. Mantenha atualizado conforme novos bounded contexts são criados

---

# GLOSSARY: [Nome do Projeto]

**Projeto:** [nome do SaaS]
**Versão:** 1.0
**Atualizado em:** [data]

---

## Instrução para AI

Ao receber este arquivo, use **exclusivamente** os termos definidos aqui para nomear entidades, eventos, comandos, queries, value objects e serviços. Se precisar de um conceito não listado, pergunte ao usuário antes de inventar um nome.

---

## 1. Mapa de Bounded Contexts

> Descreva os domínios do sistema e como se relacionam.

```
┌─────────────────┐     eventos      ┌─────────────────┐
│      [auth]     │ ──────────────→  │    [billing]    │
│  Account, User  │                  │  Subscription,  │
│  Session, Role  │                  │  Invoice, Plan  │
└─────────────────┘                  └─────────────────┘
         │                                    │
         │ eventos                            │ eventos
         ▼                                    ▼
┌─────────────────┐                  ┌─────────────────┐
│   [tenant]      │                  │  [notification] │
│  Tenant,        │                  │  Notification,  │
│  Workspace      │                  │  Channel        │
└─────────────────┘                  └─────────────────┘
```

**Regra:** Contextos se comunicam via eventos de domínio — nunca compartilham entidades diretamente.

---

## 2. Glossário por Bounded Context

### 2.1 [Nome do Bounded Context 1]

> Preencha um bounded context por seção. Duplique a seção quantas vezes for necessário.

| Termo (use no código) | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **[Termo]** | [O que significa no contexto do negócio] | [Sinônimos técnicos incorretos] | [Onde aparece: entidade, evento, etc.] |
| **Subscription** | Contrato ativo entre um Tenant e um Plano de serviço, com ciclo de cobrança | UserPlan, ServiceContract, License | Entidade: `Subscription`, Evento: `SubscriptionActivated` |
| **Plan** | Configuração de funcionalidades e preço oferecida ao mercado | Package, Bundle, Tier | Value Object: `PlanId`, Entidade: `Plan` |
| **Invoice** | Documento de cobrança gerado a cada ciclo de renovação | Bill, Receipt, Charge | Entidade: `Invoice`, Evento: `InvoiceIssued` |

### 2.2 [Nome do Bounded Context 2]

| Termo (use no código) | Definição de negócio | Termos a EVITAR | Exemplo de uso |
|---|---|---|---|
| **[Termo]** | [definição] | [evitar] | [uso] |

---

## 3. Termos SaaS Comuns (pré-preenchidos)

Estes termos são padrão para SaaS. Inclua-os no glossário do projeto ou redefina se necessário.

| Termo | Definição | Bounded Context |
|---|---|---|
| **Tenant** | Organização ou empresa que contrata o serviço; unidade máxima de isolamento de dados | tenant |
| **Workspace** | Ambiente de trabalho dentro de um Tenant (usado quando um Tenant pode ter múltiplos ambientes) | tenant |
| **Account** | Usuário individual com credenciais de acesso | auth |
| **Role** | Conjunto de permissões atribuído a um Account dentro de um Tenant | auth |
| **Subscription** | Contrato ativo de uso do serviço com ciclo de cobrança | billing |
| **Plan** | Conjunto de features e limites oferecido por um preço | billing |
| **Invoice** | Documento de cobrança gerado por ciclo de renovação | billing |
| **Trial** | Período de uso gratuito sem cobrança, limitado por tempo | billing |
| **Feature Flag** | Interruptor que habilita/desabilita uma funcionalidade por Tenant ou Plano | shared |
| **Onboarding** | Processo de criação e configuração inicial de um novo Tenant | tenant |
| **Unit of Work** | Interface que agrupa dois ou mais repositórios em uma única transação atômica; definida no domínio/shared, implementada na infraestrutura | shared |
| **Outbox Event** | Evento de domínio persistido na tabela `outbox_events` na mesma transação do aggregate, publicado de forma assíncrona por um worker | shared |
| **Job Use Case** | Use Case executado de forma assíncrona por um scheduler/worker, sem contexto HTTP; segue as mesmas regras de Use Cases comuns | application |
| **Health Check** | Endpoint sem autenticação que expõe o estado de saúde do serviço (`/health/live` e `/health/ready`) para orchestrators de container | infrastructure |

---

## 4. Convenções de Nomenclatura

### Entidades
- PascalCase
- Substantivo singular
- Exemplo: `Subscription`, `Invoice`, `WorkspaceMember`

### Value Objects
- PascalCase + sufixo descritivo quando necessário
- Exemplos: `Email`, `Money`, `SubscriptionId`, `TenantSlug`

### Eventos de Domínio
- PascalCase
- Formato: `[Entidade][Verbo no passado]`
- Exemplos: `SubscriptionActivated`, `InvoicePaid`, `TenantSuspended`

### Commands (Use Cases de escrita)
- PascalCase
- Formato: `[Verbo][Entidade]Command` ou `[Verbo][Entidade]UseCase`
- Exemplos: `CancelSubscriptionCommand`, `CreateInvoiceUseCase`

### Queries (Use Cases de leitura)
- PascalCase
- Formato: `[Get/List/Find][Entidade][Contexto]Query`
- Exemplos: `GetSubscriptionByIdQuery`, `ListTenantInvoicesQuery`

### Job Use Cases (processamento assíncrono)
- PascalCase
- Formato: `[Verbo][Entidade]Job` ou `[Verbo][Entidade]JobUseCase`
- Exemplos: `RenewSubscriptionsJob`, `GenerateMonthlyInvoicesJob`, `PurgeExpiredDataJob`

### Interfaces de Repositório
- PascalCase
- Formato: `I[Entidade]Repository`
- Exemplos: `ISubscriptionRepository`, `IInvoiceRepository`

### Error Codes
- SCREAMING_SNAKE_CASE
- Formato: `[DOMÍNIO]_[ENTIDADE]_[CONDIÇÃO]`
- Exemplos: `BILLING_SUBSCRIPTION_ALREADY_CANCELED`, `AUTH_TOKEN_EXPIRED`, `TENANT_NOT_FOUND`

---

## 5. Termos Proibidos (Anti-Ubiquitous Language)

Termos genéricos que devem ser **substituídos** pelos termos do glossário:

| Termo proibido | Use no lugar |
|---|---|
| `User` (em billing) | `Account` (auth) ou `TenantMember` (tenant) |
| `Record` | Use o nome da entidade de negócio |
| `Data` | Use o nome do conceito de negócio |
| `Manager` | Use o papel real (ex: `Subscription` em vez de `SubscriptionManager`) |
| `Handler` | Especifique o que trata (ex: `PaymentFailedHandler`) |
| `Utils`, `Helper`, `Common` | Extraia para o conceito correto de domínio ou `shared/` |
| `Info`, `Details` | Use o nome do Value Object ou DTO correto |
| `Status` como entidade | Use o estado correto da entidade (ex: `SubscriptionStatus`) |

---

## 6. Changelog do Glossário

> Registre aqui mudanças importantes nos termos — renomeações podem impactar o código.

| Data | Mudança | Motivo | Impacto no código |
|---|---|---|---|
| [data] | [ex: Renomeado `License` para `Subscription`] | [alinhamento com equipe de negócio] | [arquivos afetados] |
