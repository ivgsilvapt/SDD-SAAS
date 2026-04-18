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

> **RICE Score** = (Reach × Impact × Confidence) ÷ Effort
> - Reach: quantos usuários/tenants afeta por mês (número)
> - Impact: impacto na North Star Metric (3=massivo, 2=alto, 1=médio, 0.5=baixo, 0.25=mínimo)
> - Confidence: confiança na estimativa (1.0=alta, 0.8=média, 0.5=baixa)
> - Effort: semanas de pessoa necessárias (número)
> Use RICE para repriorizar backlog quando houver dúvida. Features com RICE baixo e sem hipótese validada vão para o Parking Lot.

| Feature | Arquivo SPEC | Status | RICE Score | Hipótese a validar | SPRINTs estimados | Dependências |
|---|---|---|---|---|---|---|
| [ex: Cadastro de Tenant e Usuário Admin] | [ex: specs/auth/register-tenant.md] | [ex: concluído] | — | — (fundação técnica) | 4 | — |
| [ex: Autenticação JWT multi-tenant] | [ex: specs/auth/authenticate-user.md] | [ex: concluído] | — | — (fundação técnica) | 3 | Cadastro de Tenant |
| [ex: Criar Plano de Ação 5W2H] | [ex: specs/action-plan/create-action-plan.md] | [ex: em-dev] | [ex: 48] | [ex: Usuários querem criar planos estruturados — validada em entrevistas] | 5 | Autenticação JWT |
| [ex: Notificação de prazo por e-mail] | [ex: specs/notification/send-deadline-alert.md] | [ex: em-spec] | [ex: 32] | [ex: Notificações aumentam taxa de conclusão ≥15%] | 3 | Criar Plano de Ação |
| [ex: Dashboard de acompanhamento] | — | backlog | [ex: 28] | [ex: Gestores precisam de visão consolidada sem abrir cada plano] | 4 | Criar Plano de Ação |
| [ex: Exportação de relatório PDF] | — | backlog | [ex: 12] | [ex: Necessidade de exportação para auditoria interna] | 3 | Dashboard |

---

## Histórico de Milestones

| Milestone | Concluído em | Principais entregas |
|---|---|---|
| [ex: Fundação Técnica] | [ex: 2025-09-15] | [ex: Setup do projeto, CI/CD, auth básica, primeiro tenant criado] |

---

## Experimentos em Andamento

> Experimentos são hipóteses sendo validadas com dados reais, antes de virar SPEC completo.
> Um experimento tem data de início, hipótese, critério de sucesso e data de decisão.
> Se o critério for atingido → cria SPEC. Se não for → move para Parking Lot.

| Experimento | Hipótese | Início | Data de decisão | Critério de sucesso | Status |
|---|---|---|---|---|---|
| [ex: Botão "Criar plano via template"] | [ex: Templates reduzem o tempo de criação em 40%] | [ex: 2025-11-01] | [ex: 2025-11-30] | [ex: 60% dos novos planos criados com template em 30 dias] | [em andamento / concluído / cancelado] |
| [ex: Banner de trial expirando] | [ex: Aviso 3 dias antes aumenta conversão em 10%] | [ex: 2025-12-01] | [ex: 2025-12-31] | [ex: Taxa de conversão trial→pago ≥ 10% maior no grupo com banner] | [em andamento] |

---

## Parking Lot — Ideias Adiadas

> Ideias válidas que chegaram cedo demais. Registradas aqui para não serem esquecidas e para evitar re-discussão.
> O Agente Spec deve verificar esta lista antes de criar novas features para evitar duplicatas.

| Data | Ideia | RICE estimado | Por que adiada | Revisitar quando |
|---|---|---|---|---|
| [ex: 2025-09-20] | [ex: Mobile app nativo iOS/Android] | [ex: 8] | [ex: Web-first até atingir product-market fit; nativo adiciona custo sem validação] | [ex: Quando atingir 500 tenants ativos pagantes] |
| [ex: 2025-10-05] | [ex: Integração com Slack para notificações] | [ex: 14] | [ex: E-mail suficiente para MVP; Slack requer OAuth + webhook complexo] | [ex: Quando feedback de usuários indicar demanda por Slack] |
