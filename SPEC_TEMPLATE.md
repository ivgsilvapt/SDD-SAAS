# SPEC_TEMPLATE.md

Use este template para criar SPECs em `specs/[dominio]/[nome-da-feature].md`.

**Convenção de nome:** `specs/[bounded-context]/[verbo]-[substantivo].md`
Exemplos: `specs/billing/create-subscription.md`, `specs/auth/reset-password.md`

Remova seções marcadas como opcionais se não se aplicarem. Não deixe campos em branco — preencha com "n/a" se necessário.

---

# SPEC: [Nome da Funcionalidade]

**Bounded Context:** [ex: billing]
**Domínio(s) afetado(s):** [ex: subscription, payment]
**Versão:** 1.0
**Status:** `rascunho` | `aprovado` | `em desenvolvimento` | `concluído`
**SPEC criado em:** [data]
**Aprovado em:** [data ou "pendente"]
**Depende de:** [outros SPECs necessários ou "nenhum"]

---

## Visão Geral

[2 a 4 frases. O que esta funcionalidade faz, por que existe e qual problema resolve. Escreva na linguagem do domínio — use Ubiquitous Language.]

---

## Hipóteses de Negócio *(obrigatório para P1; opcional para P2/P3)*

> Cada FR de prioridade P1 deve declarar qual hipótese de negócio valida.
> Uma hipótese é falsificável: tem uma condição de sucesso mensurável e um prazo para medição.
> Hipóteses derivam do `DISCOVERY.md` (se existir) ou são declaradas aqui pela primeira vez.

| FR | Hipótese que valida | Evento de medição | Critério de sucesso | Prazo |
|---|---|---|---|---|
| FR-001 | [ex: usuários querem acompanhar planos de ação em tempo real] | [ex: evento `action_plan_viewed` após criação] | [ex: 60% dos planos criados são visualizados em 48h] | [ex: 30 dias após release] |
| FR-002 | [ex: notificações aumentam taxa de conclusão de tarefas] | [ex: `task_completed` com `source: notification`] | [ex: taxa de conclusão ≥ 15% maior no grupo com notificação] | [ex: 45 dias após release] |

---

## Métricas de Sucesso do SPEC

> Como saberemos que esta feature funcionou após o lançamento?
> Defina antes de implementar — métricas definidas depois do lançamento são "metrics to justify", não "metrics to learn".
> Separe métricas de negócio (impacto real) de métricas de implementação (testes, coverage).

| Tipo | Métrica | Baseline atual | Meta após release | Como medir |
|---|---|---|---|---|
| **Negócio** | [ex: taxa de conclusão de planos de ação] | [ex: 42%] | [ex: ≥ 55%] | [ex: evento `action_plan_completed` / `action_plan_created`] |
| **Qualidade** | [ex: taxa de erro do endpoint POST /action-plans] | [ex: novo endpoint] | [ex: < 0.1%] | [ex: ratio 5xx / total no dashboard] |
| **Performance** | [ex: latência p95 de GET /action-plans] | [ex: novo endpoint] | [ex: < 300ms] | [ex: trace no APM] |

---

## Impacto em UX *(obrigatório quando camada Presentation é afetada)*

> Descreva quais telas existentes são modificadas e quais são novas.
> Liste os fluxos de usuário afetados e os pontos de entrada.
> Não é necessário wireframe detalhado — é suficiente descrever o fluxo textualmente.

**Telas afetadas:**
- [ex: `/dashboard` — adiciona card de resumo de planos ativos]
- [ex: `/action-plans/new` — nova tela de criação]

**Fluxo principal:**
[ex: Usuário acessa `/action-plans` → clica em "Novo plano" → preenche formulário 5W2H → salva → retorna à listagem com plano recém-criado visível]

**Fluxos de erro:**
[ex: Campos obrigatórios vazios → mensagem de validação inline, foco no primeiro campo inválido]

**Design tokens / componentes novos:**
[ex: nenhum — usa componentes existentes do Design System | ex: novo componente `ActionStatusBadge`]

---

## User Stories

> Prioridades: **P1** = crítica (bloqueia valor), **P2** = importante (entrega valor significativo), **P3+** = desejável (melhoria).
> Cada story deve ser independentemente testável e entregar valor isolado.

| ID | Prioridade | Story |
|---|---|---|
| US-01 | P1 | Como [quem], quero [o quê], para [por quê] |
| US-02 | P2 | Como [quem], quero [o quê], para [por quê] |

---

## Requisitos Não-Funcionais (NFRs)

> Liste expectativas de performance, segurança, disponibilidade e escala que afetam design ou arquitetura.
> NFR sem critério mensurável é inútil — todo NFR deve ter como medir.

| ID | Categoria | Requisito | Critério de Aceitação |
|---|---|---|---|
| NFR-001 | Performance | [ex: listagem retorna em até 200ms no p95] | [ex: medido com 10k registros no banco de teste] |
| NFR-002 | Segurança | [ex: apenas admin pode cancelar assinatura de outro usuário] | [teste de autorização com role não-admin retorna 403] |
| NFR-003 | Disponibilidade | [ex: endpoint crítico < 0.1% de erro] | [alerta se taxa de erro superar 0.1% em janela de 5min] |
| NFR-004 | Escala | [ex: suporta 1.000 tenants ativos simultâneos] | [load test com N tenants sem degradação] |

---

## Requisitos Funcionais

> Cada requisito deve ser rastreável a pelo menos uma User Story e ter ao menos um cenário de aceitação.
> Use `[NEEDS CLARIFICATION]` para requisitos com ambiguidades — documente-as na seção Clarify abaixo.

| ID | Descrição | User Story | Prioridade |
|---|---|---|---|
| FR-001 | [descrição objetiva do requisito] | US-01 | P1 |
| FR-002 | [descrição objetiva do requisito] | US-01 | P1 |
| FR-003 | [descrição objetiva do requisito — ou [NEEDS CLARIFICATION]] | US-02 | P2 |

---

## Clarify — Ambiguidades a Resolver

> **Regra (spec-kit):** Não escreva os Critérios de Aceitação nem inicie nenhum SPRINT enquanto houver itens não resolvidos aqui.
> Para cada ambiguidade: descreva a dúvida, o impacto se não resolvida e a decisão tomada após resolução.

| # | Ambiguidade | FR relacionado | Impacto | Decisão / Resposta |
|---|---|---|---|---|
| 1 | [descreva a dúvida] | FR-00X | [o que quebra se não resolvida] | [pendente / decisão tomada] |

---

## Critérios de Aceitação

> Formato Given-When-Then por requisito funcional. Descreva comportamento observável — não implementação.

### FR-001 — [Título curto]

**Cenário principal:**
- **Dado** [estado inicial do sistema / contexto]
- **Quando** [ação executada pelo usuário ou sistema]
- **Então** [resultado observável esperado]

**Cenário alternativo / exceção:** *(se aplicável)*
- **Dado** [contexto alternativo]
- **Quando** [mesma ação ou ação diferente]
- **Então** [resultado esperado no caso alternativo]

### FR-002 — [Título curto]

**Cenário principal:**
- **Dado** [contexto]
- **Quando** [ação]
- **Então** [resultado]

---

## Checklist de Cobertura

> Valida que cada FR tem pelo menos um cenário de aceitação e está mapeado a uma User Story.
> Execute após resolver todas as ambiguidades e antes de iniciar qualquer SPRINT.

| FR | Tem User Story? | Tem cenário Given-When-Then? | Cenário é testável independentemente? |
|---|---|---|---|
| FR-001 | [ ] | [ ] | [ ] |
| FR-002 | [ ] | [ ] | [ ] |
| FR-003 | [ ] | [ ] | [ ] |

---

## Contexto Arquitetural

| Campo | Valor |
|---|---|
| **Camadas afetadas** | [domain / application / infrastructure / presentation] |
| **Domínio já modelado** | [sim / não — se não, SPRINT 1 é obrigatório antes de qualquer outro] |
| **Multi-tenant** | [sim / não — se sim, consulte SAAS_PATTERNS.md antes de modelar] |
| **Eventos de domínio gerados** | [lista ou "nenhum"] |
| **Bounded contexts relacionados** | [lista ou "nenhum"] |
| **Comunicação entre contextos** | [via eventos de domínio / via query / nenhuma] |
| **Integrações externas necessárias** | [ex: gateway de pagamento, serviço de e-mail, ou "nenhuma"] |
| **Feature flags necessárias** | [lista ou "nenhuma"] |
| **PII envolvido** | [campos com dados pessoais ou "nenhum"] |

---

## SPRINTs

> **Ordem obrigatória (Domain-First):** Domain → Application → Infrastructure → Presentation → Cross-cutting.
> Não inicie um SPRINT externo antes de concluir e validar o SPRINT interno.
> Cada SPRINT indica quais FRs implementa — não implemente FRs não listados no SPRINT.

---

## SPRINT 1 — Domínio

**Objetivo:** Modelar entidades, value objects, eventos e interfaces de repositório. Zero dependências externas.
**FRs implementados:** [ex: FR-001, FR-002]
**Para implementar:** `/impl-sprint specs/[dominio]/[feature].md 1` *(aplique TDD: Plano de Testes guia o ciclo Red → Green → Refactor por FR)*

### Entidades

| Nome | Atributos (nome: tipo) | Comportamentos (método: descrição) |
|---|---|---|
| [Nome] | [campo: tipo] | [método(): o que faz] |

### Value Objects

| Nome | Atributos | Validações / Invariantes |
|---|---|---|
| [Nome] | [campo: tipo] | [regra de validação] |

### Eventos de Domínio

| Nome | Payload | Quando é disparado |
|---|---|---|
| [NomeEvento] | [campos] | [condição que dispara] |

### Interfaces de Repositório

```
interface [Nome]Repository {
  [nomeMetodo(parametro: Tipo): TipoRetorno]
}
```

### Impacto em Banco de Dados

| Tabela | Operação | Colunas principais | Migration necessária |
|---|---|---|---|
| [nome_tabela] | CREATE / ALTER | [campo: tipo, ...] | [nome do arquivo de migration] |

### Critérios de Aceitação — SPRINT 1

- [ ] Entidades em `src/domain/[dominio]/entities/`
- [ ] Value Objects em `src/domain/[dominio]/value-objects/`
- [ ] Eventos em `src/domain/[dominio]/events/`
- [ ] Interfaces de repositório em `src/domain/[dominio]/repositories/`
- [ ] Nenhum arquivo de domínio importa de `infrastructure/`, ORM ou biblioteca externa
- [ ] Todos os nomes usam Ubiquitous Language definida na Visão Geral
- [ ] Entidades têm comportamentos — não são apenas estruturas de dados (evitar Anemic Domain Model)
- [ ] Erros de negócio retornam Result<T, E> com error code — sem null silencioso

### Plano de Testes — SPRINT 1

> **TDD:** Estes testes são escritos **antes** da implementação de cada FR (ciclo Red → Green → Refactor). O Agente Testing valida a cobertura completa após o SPRINT.

| Teste | Tipo | FR coberto | Cenário GWT |
|---|---|---|---|
| [ex: Subscription_Cancel_WhenActive_ShouldReturnCanceled] | unit/domain | FR-001 | Cenário principal |
| [ex: Subscription_Cancel_WhenAlreadyCanceled_ShouldReturnError] | unit/domain | FR-001 | Cenário alternativo |

---

## SPRINT 2 — Application

**Objetivo:** Implementar os casos de uso que orquestram o domínio. Esta camada abre e fecha transações.
**FRs implementados:** [ex: FR-001, FR-003]
**Para implementar:** `/impl-sprint specs/[dominio]/[feature].md 2` *(aplique TDD: Plano de Testes guia o ciclo Red → Green → Refactor por FR)*

### Commands (escrita — modifica estado)

| Nome do Command | Dados de Entrada | Resultado Esperado | Requer Transação |
|---|---|---|---|
| [NomeCommand] | [campo: tipo] | [o que retorna ou dispara] | sim / não |

### Queries (leitura — não modifica estado)

| Nome da Query | Filtros / Parâmetros | Dados Retornados |
|---|---|---|
| [NomeQuery] | [campo: tipo] | [estrutura do resultado] |

### Critérios de Aceitação — SPRINT 2

- [ ] Commands em `src/application/[dominio]/commands/`
- [ ] Queries em `src/application/[dominio]/queries/`
- [ ] Transações abertas e fechadas apenas nos Use Cases — nunca no Controller ou Domínio
- [ ] Use Cases delegam regras de negócio ao Domínio — não as reimplementam
- [ ] Nenhum Use Case importa diretamente de `infrastructure/`
- [ ] Commands e Queries não fazem leitura e escrita no mesmo método (CQS)
- [ ] TenantContext injetado via DI nos Use Cases (se multi-tenant)

### Plano de Testes — SPRINT 2

> **TDD:** Estes testes são escritos **antes** da implementação de cada FR (ciclo Red → Green → Refactor). O Agente Testing valida a cobertura completa após o SPRINT.

| Teste | Tipo | FR coberto | Cenário GWT |
|---|---|---|---|
| [ex: CancelSubscriptionUseCase_Execute_ShouldPersistCanceled] | unit/application | FR-001 | Cenário principal |
| [ex: CancelSubscriptionUseCase_Execute_WhenNotFound_ShouldReturnError] | unit/application | FR-001 | Cenário alternativo |

---

## SPRINT 3 — Infraestrutura

**Objetivo:** Implementar as interfaces definidas no domínio e conectar serviços externos.
**FRs implementados:** [ex: FR-001, FR-002]
**Para implementar:** `/impl-sprint specs/[dominio]/[feature].md 3`

### Implementações de Repositório

| Interface (domínio) | Classe de Implementação | Tecnologia / ORM |
|---|---|---|
| [InterfaceRepository] | [ConcreteRepository] | [ex: Prisma, TypeORM] |

### Integrações Externas *(opcional — remova se não aplicável)*

| Serviço | Interface no Domínio | Classe de Implementação | Biblioteca |
|---|---|---|---|
| [ex: e-mail] | [IMailer] | [SendGridMailer] | [sendgrid] |

### Impacto em Banco de Dados

| Tabela | Operação | Detalhes | Migration necessária |
|---|---|---|---|
| [nome_tabela] | CREATE / ALTER / ADD INDEX | [detalhes] | [nome do arquivo de migration] |

### Critérios de Aceitação — SPRINT 3

- [ ] Implementações de repositório em `src/infrastructure/database/repositories/`
- [ ] Implementações de serviços externos em `src/infrastructure/[servico]/`
- [ ] Implementações referenciam interfaces do domínio — não as reimplementam
- [ ] Nenhum detalhe de infraestrutura (SQL, nome de tabela, schema) vaza para domínio ou application
- [ ] Serviços externos são instanciados via DI — nunca com `new` direto nos Use Cases
- [ ] Todo repositório filtra por `tenantId` em toda query (se multi-tenant)
- [ ] Migrations em `src/infrastructure/database/migrations/` com nomenclatura correta

### Plano de Testes — SPRINT 3

> **Agente Testing:** Estes testes de integração são gerados pelo Agente Testing após a implementação (setup de banco real dificulta o ciclo TDD).

| Teste | Tipo | FR coberto | O que valida |
|---|---|---|---|
| [ex: SubscriptionRepository_FindById_ShouldReturnSubscription] | integration/infrastructure | FR-001 | Query real + mapeamento ORM |
| [ex: SubscriptionRepository_FindById_ShouldNotReturnOtherTenantData] | integration/infrastructure | Segurança | Isolamento de tenant |

---

## SPRINT 4 — Apresentação

**Objetivo:** Implementar validação de entrada, controller, viewmodel, view e chaves de tradução.
**FRs implementados:** [ex: FR-001, FR-002, FR-003]
**Para implementar:** `/impl-sprint specs/[dominio]/[feature].md 4`

### Command Object — Validação de Entrada

| Campo | Tipo | Regra de Validação | Mensagem de Erro (chave i18n) |
|---|---|---|---|
| [campo] | [tipo] | [regra] | [error.campo.regra] |

### Contrato de API

| Método | Rota | Auth | Request Body | Response 2xx | Errors possíveis |
|---|---|---|---|---|---|
| POST | /api/v1/[recurso] | Bearer JWT | [campos] | 201 + [ViewModel] | 400, 401, 403, 409, 422 |
| GET | /api/v1/[recurso]/:id | Bearer JWT | — | 200 + [ViewModel] | 401, 403, 404 |

### Controller

| Rota | Método HTTP | Chama (Use Case) | Retorna |
|---|---|---|---|
| [/rota] | [GET/POST/etc] | [NomeUseCase] | [ViewModel ou status] |

### ViewModel

| Campo | Tipo | Origem (entidade / use case) |
|---|---|---|
| [campo] | [tipo] | [de onde vem] |

### Estrutura da View *(opcional — remova para APIs puras)*

[Descreva a estrutura da view: formulários, tabelas, cards. Mencione quais dados exibe e quais ações permite.]

### Chaves i18n

| Chave | Valor pt-BR | Valor en |
|---|---|---|
| [contexto.elemento.estado] | [tradução] | [translation] |

### Critérios de Aceitação — SPRINT 4

- [ ] Command Object em `src/presentation/input/`
- [ ] Controller em `src/presentation/controllers/` — sem lógica de negócio
- [ ] ViewModel em `src/presentation/viewmodels/` — não expõe entidades de domínio diretamente
- [ ] Zero texto literal visível ao usuário na view sem chave i18n correspondente
- [ ] Chaves i18n adicionadas em todos os arquivos de locale configurados
- [ ] Controller valida entrada via Command Object antes de chamar o Use Case (Fail Fast)
- [ ] Controller verifica autorização RBAC antes de chamar o Use Case
- [ ] Error codes mapeados para HTTP status correto
- [ ] Contrato de API implementado conforme tabela acima

### Plano de Testes — SPRINT 4

> **Agente Testing:** Estes testes de integração são gerados pelo Agente Testing após a implementação (setup de HTTP client dificulta o ciclo TDD).

| Teste | Tipo | FR coberto | O que valida |
|---|---|---|---|
| [ex: POST_subscriptions_ShouldReturn201] | integration/presentation | FR-001 | Status code + body |
| [ex: POST_subscriptions_WithoutToken_ShouldReturn401] | integration/presentation | Segurança | Autenticação obrigatória |
| [ex: POST_subscriptions_WithInvalidInput_ShouldReturn422] | integration/presentation | FR-001 | Validação de input |

---

## SPRINT 5 — Aspectos Transversais *(opcional — remova se não aplicável)*

**Objetivo:** Adicionar middleware, logging específico ou regras de segurança desta funcionalidade.
**FRs implementados:** [ex: n/a ou FR-003]
**Para implementar:** `/impl-sprint specs/[dominio]/[feature].md 5`

### Middleware / Interceptadores

| Nome | Evento de Aplicação | Comportamento |
|---|---|---|
| [NomeMiddleware] | [antes/depois de qual operação] | [o que faz] |

### Critérios de Aceitação — SPRINT 5

- [ ] Middleware em `src/presentation/middleware/`
- [ ] Lógica transversal não está inline em nenhuma camada de negócio
- [ ] Logging e auditoria aplicados via aspecto — não duplicados em múltiplos lugares

### Plano de Testes — SPRINT 5

> **Agente Testing:** Estes testes são gerados pelo Agente Testing após a implementação do middleware.

| Teste | Tipo | O que valida |
|---|---|---|
| [ex: RateLimitMiddleware_WhenLimitExceeded_ShouldReturn429] | integration/presentation | Comportamento do middleware |

---

## Analyze — Validação Cruzada Pré-Implementação

> Execute antes do primeiro `/impl-sprint`. Use `/review-arch [arquivo] analyze` ou o Agente Analyze.
> Bloqueia a implementação se houver inconsistências entre os artefatos abaixo.

| Verificação | Pergunta | OK? |
|---|---|---|
| **SPEC × Constitution** | Os FRs e User Stories respeitam as restrições do ARCHITECTURE.md? | [ ] |
| **FRs × Cenários** | Cada FR tem pelo menos um cenário Given-When-Then rastreável? | [ ] |
| **FRs × SPRINTs** | Cada FR aparece em pelo menos um SPRINT? Algum SPRINT referencia FR inexistente? | [ ] |
| **SPRINTs × Camadas** | Cada SPRINT opera apenas na sua camada? Sem acesso antecipado a camadas externas? | [ ] |
| **Contexto Arquitetural × Domínio** | As entidades e interfaces modeladas no SPRINT 1 cobrem todos os FRs listados? | [ ] |
| **NFRs × SPRINTs** | Cada NFR tem critério mensurável e está endereçado em algum SPRINT? | [ ] |
| **API Contract × FRs** | O Contrato de API do SPRINT 4 cobre todos os FRs de apresentação? | [ ] |
| **Plano de Testes × Cenários GWT** | Cada cenário GWT tem pelo menos um teste planejado no Plano de Testes? | [ ] |
| **Impacto em Banco × Entidades** | As migrations planejadas nos SPRINTs 1 e 3 cobrem todas as entidades modeladas? | [ ] |
| **i18n × View** | Todas as strings visíveis ao usuário têm chave i18n definida na tabela do SPRINT 4? | [ ] |
| **Hipóteses × FRs P1** | Cada FR de prioridade P1 declara qual hipótese valida e como medir? | [ ] |
| **Métricas × Hipóteses** | As métricas de sucesso são mensuráveis e têm baseline e meta definidos? | [ ] |
| **Clarify** | Todas as ambiguidades foram resolvidas? | [ ] |

> **Regra:** Só inicie os SPRINTs após todos os itens marcados. Inconsistências identificadas aqui devem ser corrigidas no SPEC antes da implementação.

---

## Checklist Final

Execute `/review-arch` após concluir todos os sprints. Só marque como `concluído` após todos os itens abaixo:

- [ ] Checklist de Cobertura completo (todos os FRs com story e cenário)
- [ ] Analyze executado — sem inconsistências entre artefatos
- [ ] Todos os critérios de aceitação de cada SPRINT satisfeitos
- [ ] Todos os Planos de Testes executados — cobertura GWT completa
- [ ] `/review-arch` executado — nenhuma violação crítica reportada
- [ ] Cenários Given-When-Then validados por testes automatizados
- [ ] NFRs validados (performance medida, segurança testada)
- [ ] Chaves i18n adicionadas em todos os locales
- [ ] Migrations executadas e testadas em ambiente de staging
- [ ] Hipóteses de negócio registradas com evento de medição configurado (tracking implementado)
- [ ] Métricas de sucesso com baseline registrado antes do release
- [ ] SPEC atualizado: `Status: concluído` e `Aprovado em:` preenchido
