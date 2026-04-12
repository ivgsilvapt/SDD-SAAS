# ROADMAP.md — Roadmap de Features

> **Como usar:** Copie para `ROADMAP.md` na raiz do seu projeto SaaS.
> Atualizado a cada feature iniciada, concluída ou repriorizada.
> Status possíveis: `backlog` | `em-spec` | `em-dev` | `em-review` | `concluído`

---

## Milestone Atual

**Nome:** [ex: MVP — Controle de Planos de Ação]
**Meta:** [ex: Ter o fluxo completo de criação, atribuição e acompanhamento de ações funcionando para os primeiros 10 tenants beta]
**Critérios de sucesso:**
- [ ] [ex: Tenant consegue criar plano de ação com pelo menos 3 campos 5W2H]
- [ ] [ex: Responsável recebe notificação por e-mail ao ser atribuído]
- [ ] [ex: Gestor vê painel consolidado com status de todas as ações do tenant]

---

## Features por Status

| Feature | Arquivo SPEC | Status | Prioridade | SPRINTs estimados | Dependências |
|---|---|---|---|---|---|
| [ex: Cadastro de Tenant e Usuário Admin] | [ex: specs/auth/register-tenant.md] | [ex: concluído] | P1 | 4 | — |
| [ex: Autenticação JWT multi-tenant] | [ex: specs/auth/authenticate-user.md] | [ex: concluído] | P1 | 3 | Cadastro de Tenant |
| [ex: Criar Plano de Ação 5W2H] | [ex: specs/action-plan/create-action-plan.md] | [ex: em-dev] | P1 | 5 | Autenticação JWT |
| [ex: Notificação de prazo por e-mail] | [ex: specs/notification/send-deadline-alert.md] | [ex: em-spec] | P2 | 3 | Criar Plano de Ação |
| [ex: Dashboard de acompanhamento] | — | backlog | P2 | 4 | Criar Plano de Ação |
| [ex: Exportação de relatório PDF] | — | backlog | P3 | 3 | Dashboard |

---

## Histórico de Milestones

| Milestone | Concluído em | Principais entregas |
|---|---|---|
| [ex: Fundação Técnica] | [ex: 2025-09-15] | [ex: Setup do projeto, CI/CD, auth básica, primeiro tenant criado] |

---

## Parking Lot — Ideias Adiadas

> Ideias válidas que chegaram cedo demais. Registradas aqui para não serem esquecidas e para evitar re-discussão.
> O Agente Spec deve verificar esta lista antes de criar novas features para evitar duplicatas.

| Data | Ideia | Por que adiada | Revisitar quando |
|---|---|---|---|
| [ex: 2025-09-20] | [ex: Mobile app nativo iOS/Android] | [ex: Web-first até atingir product-market fit; nativo adiciona custo sem validação] | [ex: Quando atingir 500 tenants ativos pagantes] |
| [ex: 2025-10-05] | [ex: Integração com Slack para notificações] | [ex: E-mail suficiente para MVP; Slack requer OAuth + webhook complexo] | [ex: Quando feedback de usuários indicar demanda por Slack] |
