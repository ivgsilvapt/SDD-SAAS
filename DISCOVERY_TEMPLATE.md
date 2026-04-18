# DISCOVERY.md — Validação de Problema

> **Como usar:** Copie para `DISCOVERY.md` na raiz do projeto, ou para `specs/[dominio]/DISCOVERY.md` para uma feature específica.
> Preenchido pelo Agente Discovery via `/discover [ideia]` ou manualmente antes do primeiro SPEC.
> **Regra:** Nenhum SPEC de feature P1 deve ser criado antes de as hipóteses principais estarem marcadas como `validada com evidência`.

---

**Ideia original:** [descreva a ideia em 1–2 frases]
**Data:** [YYYY-MM-DD]
**Status:** `em validação` | `problema validado` | `requer mais pesquisa` | `pivotar`

---

## 1. Diagnóstico do Problema — 5 Porquês

> Aplique os 5 Porquês para chegar à causa raiz. Cada "porque" deve ser mais profundo que o anterior.
> Pare quando chegar a algo que você pode influenciar diretamente com produto.

**Problema declarado:** [ex: "Minha equipe não cumpre os planos de ação"]

| # | Por que? | Resposta |
|---|---|---|
| 1 | Por que o problema declarado acontece? | [ex: Porque as pessoas esquecem das tarefas atribuídas] |
| 2 | Por que elas esquecem? | [ex: Porque as tarefas ficam em planilhas que ninguém abre todo dia] |
| 3 | Por que as planilhas não são abertas? | [ex: Porque não há lembretes e a planilha está sempre desatualizada] |
| 4 | Por que está desatualizada? | [ex: Porque atualizar manualmente é chato e ninguém é responsável] |
| 5 | Por que ninguém é responsável? | [ex: Porque não há uma ferramenta que torne fácil e visível quem deve atualizar] |

**Causa raiz identificada:** [ex: Falta de ferramenta que torne a atualização fácil e visível para os responsáveis]

---

## 2. Personas

> Identifique 2–3 personas: quem tem o problema, quem paga e quem usa. Podem se sobrepor.
> Valide com pelo menos 3 conversas reais antes de marcar hipóteses como validadas.

### Persona 1 — [Nome fictício]

| Campo | Descrição |
|---|---|
| **Papel** | [ex: Gerente de Operações] |
| **Contexto** | [ex: Empresa industrial, 20–200 funcionários] |
| **Job to Be Done principal** | [ex: Quando começo a semana, quero ver o status de todas as ações pendentes para saber onde preciso intervir] |
| **Frequência do problema** | [ex: Diária] |
| **Alternativa atual** | [ex: Planilha Excel compartilhada no Google Drive] |
| **Frustração com a alternativa atual** | [ex: Sempre desatualizada, sem histórico, sem lembretes] |
| **Willingness to pay** | [ex: R$ 150–300/mês se resolver o problema] |
| **Evidência** | [ex: Entrevista com 5 gerentes de operações em 2025-10-15] |

### Persona 2 — [Nome fictício]

| Campo | Descrição |
|---|---|
| **Papel** | [ex: Analista de Qualidade] |
| **Contexto** | [ex: Recebe e executa tarefas via plano de ação] |
| **Job to Be Done principal** | [ex: Quando sou notificado, quero entender imediatamente o que preciso fazer e até quando] |
| **Frequência do problema** | [ex: 2–3x por semana] |
| **Alternativa atual** | [ex: WhatsApp + e-mail + planilha — 3 fontes diferentes] |
| **Frustração** | [ex: Não tem uma fonte única, fácil de perder tarefas] |
| **Evidência** | [ex: Observação de 2 analistas durante 1 semana] |

---

## 3. Lean Canvas

> Preencha os 9 blocos. Seja conciso — 1–3 itens por bloco.
> Um Lean Canvas incompleto ou com hipóteses não validadas indica que ainda não é hora de criar SPECs.

| Bloco | Conteúdo |
|---|---|
| **1. Problema** | [Top 3 problemas que o produto resolve] |
| **2. Segmento de clientes** | [Quem são os early adopters? Quem paga? Quem usa?] |
| **3. Proposta de valor única** | [Por que alguém usaria isso em vez da alternativa atual? Em uma frase.] |
| **4. Solução** | [Top 3 funcionalidades mínimas para resolver o problema] |
| **5. Canais** | [Como os clientes vão descobrir o produto? Como vão comprar?] |
| **6. Fontes de receita** | [Quanto cobrar? Por assento? Flat-rate? Por uso?] |
| **7. Estrutura de custos** | [Principais custos: infra, pagamento, suporte, aquisição] |
| **8. Métricas-chave** | [O que medir para saber se está funcionando? (North Star + 2 guardrails)] |
| **9. Vantagem injusta** | [O que você tem que é difícil de copiar? Acesso, dados, expertise?] |

---

## 4. North Star Metric e Guardrails

**North Star Metric:**
> [ex: Número de planos de ação com 100% das tarefas concluídas no prazo, por tenant, por mês]
> *Por que este número?* [ex: Representa o valor real entregue — o tenant atingiu o objetivo para o qual nos contratou]

**Guardrails (o que não pode cair mesmo que a North Star suba):**

| Guardrail | Limite | Por que é inegociável |
|---|---|---|
| [ex: Taxa de erro p/ endpoints críticos] | [ex: < 0.5%] | [ex: Confiabilidade é pré-requisito de adoção] |
| [ex: Tempo de resposta do painel] | [ex: < 500ms p95] | [ex: Painel lento torna o produto inutilizável no início do dia] |

---

## 5. Hipóteses de Negócio

> Hipóteses são afirmações falsificáveis sobre o comportamento esperado dos usuários.
> Cada hipótese tem: enunciado, experimento de validação (de menor custo possível) e critério de sucesso.
> **Apenas hipóteses marcadas como `validada com evidência` desbloqueiam criação de SPEC.**

| # | Hipótese | Tipo | Experimento | Critério de sucesso | Status | Evidência |
|---|---|---|---|---|---|---|
| H1 | [ex: Gerentes de operações pagariam por uma ferramenta de acompanhamento de planos de ação] | Negócio | [ex: 10 entrevistas + perguntar willingness to pay] | [ex: ≥ 6/10 indicam que pagariam ≥ R$ 100/mês] | `pendente` | — |
| H2 | [ex: Notificações automáticas aumentam a taxa de conclusão de tarefas] | Produto | [ex: A/B test: grupo com e-mail vs. sem] | [ex: Taxa de conclusão ≥ 15% maior no grupo com e-mail] | `pendente` | — |
| H3 | [ex: Usuários conseguem criar o primeiro plano sem onboarding guiado] | UX | [ex: Teste de usabilidade com 5 usuários — gravar sessão] | [ex: ≥ 4/5 criam plano em < 5min sem ajuda] | `pendente` | — |

**Status possíveis:**
- `pendente` — experimento não iniciado
- `em validação` — experimento em andamento
- `validada com evidência` — critério de sucesso atingido, evidência registrada
- `invalidada` — critério não atingido — considere pivotar esta hipótese
- `descartada` — hipótese não é relevante para o produto atual

---

## 6. Riscos e Incertezas

> Liste os maiores riscos que podem fazer o produto falhar.
> Para cada risco: probabilidade (1–3), impacto (1–3), e como mitigar.

| Risco | Probabilidade | Impacto | Mitigação |
|---|---|---|---|
| [ex: O problema existe, mas os usuários não pagariam por solução digital — já usam WhatsApp de graça] | 2 | 3 | [ex: Validar willingness to pay em entrevistas antes de qualquer desenvolvimento] |
| [ex: Mercado já tem concorrentes consolidados (Trello, Monday.com)] | 3 | 2 | [ex: Focar em nicho específico (indústria + 5W2H) que genéricos não atendem bem] |
| [ex: Custo de aquisição de cliente muito alto] | 2 | 3 | [ex: Começar com vendas diretas (founder-led sales) para validar ICP antes de marketing pago] |

---

## 7. Veredicto

> Preenchido pelo Agente Discovery ou pelo desenvolvedor após completar as seções acima.

**Veredicto:** `PROBLEMA VALIDADO` | `REQUER MAIS PESQUISA` | `CONSIDERAR PIVOTAR`

**Justificativa:**
[ex: 7 de 8 hipóteses estão validadas com evidência. H2 (notificações) ainda em validação mas não bloqueia o MVP.
O problema é real (confirmado em entrevistas), willingness to pay existe (R$ 180/mês em média) e há vantagem injusta (acesso direto ao nicho industrial via parceiro).]

**Próximo passo:**
- [ ] Criar `PROJECT.md` com Vision Statement, Personas e North Star derivados deste DISCOVERY
- [ ] Criar SPEC para a feature de maior RICE que valida H1 (hipótese de valor central)
- [ ] Revisitar H2 em 30 dias com dados reais do produto

---

## Links

- `PROJECT.md` — visão estratégica derivada deste DISCOVERY
- `ROADMAP.md` — features priorizadas com hipóteses vinculadas
- `specs/` — SPECs das features que validam as hipóteses acima
