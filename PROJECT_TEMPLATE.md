# PROJECT.md — Visão do Produto

> **Como usar:** Copie para `PROJECT.md` na raiz do seu projeto SaaS.
> Preenchido uma vez durante a concepção do produto, revisado a cada mudança de direção estratégica.
> O CLAUDE.md carrega-o como contexto opcional para o Agente Spec (`@PROJECT.md`).

---

## Vision Statement

> *Uma frase que define: qual problema resolve, para quem e como.*
> *Exemplo: "Ajudamos pequenas equipes de operações a substituir planilhas de 5W2H por um plano de ação digital rastreável — sem treinamento técnico."*

[Escreva aqui a vision statement do seu SaaS]

---

## Personas

> Personas concretas ajudam o Agente Spec a criar User Stories relevantes e o Agente Discovery a validar hipóteses.
> Defina ao menos 2 personas: quem paga (decisor) e quem usa (usuário final).
> Se o `DISCOVERY.md` existir, as personas devem ser derivadas de lá.

### Persona 1 — [Nome fictício, papel]

| Campo | Descrição |
|---|---|
| **Perfil** | [ex: Maria, Gerente de Operações, 38 anos, empresa industrial de 80 funcionários] |
| **Objetivo principal** | [ex: Ter visibilidade em tempo real do andamento dos planos de ação da equipe sem precisar perguntar a cada um] |
| **Maior frustração atual** | [ex: Planilhas Excel desatualizadas e sem histórico — nunca sabe se o que está vendo é a versão mais recente] |
| **Como mede sucesso** | [ex: 100% dos planos com prazo têm responsável e status atualizado] |
| **Frequência de uso** | [ex: Diária — acompanha painel no começo e fim do dia] |
| **Nível técnico** | [ex: Médio — usa ferramentas de gestão mas não é programadora] |

**Jobs to Be Done:**
- Quando [situação], quero [motivação], para [resultado esperado].
- [ex: Quando começo a semana, quero ver rapidamente quais ações estão atrasadas, para priorizar onde preciso intervir]

**Pains / Gains:**

| Pains (o que frustra) | Gains (o que ela quer ganhar) |
|---|---|
| [ex: Passar horas consolidando planilhas antes de reuniões] | [ex: Painel pronto para apresentar sem preparação manual] |
| [ex: Não saber quem é responsável por cada ação] | [ex: Rastreabilidade clara de responsável e prazo] |

---

### Persona 2 — [Nome fictício, papel]

| Campo | Descrição |
|---|---|
| **Perfil** | [ex: Carlos, Analista de Qualidade, 28 anos, recebe tarefas via plano de ação] |
| **Objetivo principal** | [ex: Saber exatamente o que precisa fazer hoje e conseguir marcar como feito sem fricção] |
| **Maior frustração atual** | [ex: Recebe tarefas por WhatsApp, e-mail e planilha — não tem uma fonte única de verdade] |
| **Como mede sucesso** | [ex: Zero tarefa esquecida ou vencida sem que ele saiba] |
| **Frequência de uso** | [ex: Quando recebe notificação ou no início do dia] |
| **Nível técnico** | [ex: Básico — usa smartphone e ferramentas simples] |

**Jobs to Be Done:**
- [ex: Quando sou notificado de uma nova tarefa, quero entender imediatamente o que precisa ser feito e até quando, para não atrasar minha equipe]

---

## North Star Metric e Guardrails

> A North Star Metric é **o único número** que melhor captura o valor entregue ao usuário.
> Se subir, o produto está funcionando. Se cair, algo está errado.
> Guardrails são limites que não podem ser sacrificados para aumentar a North Star.

**North Star Metric:**
> [ex: Número de planos de ação com 100% das tarefas concluídas no prazo, por tenant, por mês]
> *Por que este número?* [ex: Representa o valor real entregue — o tenant atingiu o objetivo para o qual contratou o produto]

**Guardrails:**
| Guardrail | Limite | Por que não pode ser sacrificado |
|---|---|---|
| [ex: Taxa de erro de endpoints críticos] | [ex: < 0.5%] | [ex: Erros frequentes destroem confiança do tenant] |
| [ex: Tempo de resposta p95 do dashboard] | [ex: < 500ms] | [ex: Dashboard lento torna o produto inutilizável no início do dia] |

---

## Público-Alvo

**Quem paga (decisor de compra):**
> *ex: Gerentes de operações de empresas com 20–200 funcionários no setor industrial*

**Quem usa (usuário final):**
> *ex: Analistas de qualidade e líderes de equipe que precisam criar e acompanhar planos de ação diariamente*

**Problema principal que resolvemos:**
> *ex: O controle de planos de ação em planilhas perde histórico, não envia lembretes e não permite visibilidade para o gestor em tempo real*

---

## Proposta de Valor

O que nos diferencia de concorrentes e alternativas (ex: planilhas, ferramentas genéricas):

1. [Diferencial 1 — ex: Notificações automáticas por prazo com zero configuração]
2. [Diferencial 2 — ex: Visão consolidada de todas as ações do tenant em um painel]
3. [Diferencial 3 — ex: Integração com sistemas de qualidade já existentes via webhook]

---

## Non-Goals (o que este SaaS NÃO faz)

> *Ser explícito sobre non-goals evita que o Agente Spec proponha features fora de escopo.*

- [ ] Não gerenciamos projetos complexos (isso é Jira/Asana — fora do escopo)
- [ ] Não oferecemos relatórios financeiros (nosso foco é operacional)
- [ ] Não integramos com ERPs nesta fase (versão 2.0 talvez)
- [Adicione os seus non-goals aqui]

---

## Decisões de Stack

Tecnologias escolhidas para este projeto e o racional de cada uma.
> *Preencha com as tecnologias reais do seu projeto.*

| Camada | Tecnologia | Versão | Racional |
|---|---|---|---|
| Linguagem | [ex: TypeScript] | [ex: 5.x] | [ex: Type safety + ecossistema Node; equipe já domina] |
| Framework | [ex: NestJS] | [ex: 10.x] | [ex: Módulos e DI nativos facilitam Clean Architecture] |
| ORM | [ex: Prisma] | [ex: 5.x] | [ex: Type-safe queries; migrations declarativas] |
| Banco | [ex: PostgreSQL] | [ex: 16] | [ex: Modelo relacional para billing; suporte nativo a UUID e JSONB] |
| Testes | [ex: Jest] | [ex: 29.x] | [ex: Padrão do ecossistema; integração com NestJS] |
| Autenticação | [ex: JWT + Passport] | — | [ex: Stateless; suporte a múltiplos tenants no payload] |

---

## Identidade Visual *(preencher se o produto tiver UI própria — usado pelo Agente Design)*

> Especificidade acima de tudo — valores exatos, não descrições vagas ("azul" não serve, `#2563EB` serve).

| Token | Valor | Uso |
|---|---|---|
| Cor primária | [ex: `#2563EB`] | Ações principais, links, elementos de destaque |
| Cor de fundo | [ex: `#0F172A`] | Fundo da aplicação |
| Cor de card/superfície | [ex: `#1E293B`] | Cards, painéis, modais |
| Cor de status positivo | [ex: `#22C55E`] | Sucesso, ativo, concluído |
| Cor de status de alerta | [ex: `#EF4444`] | Erro, bloqueio, cancelamento |
| Fonte | [ex: Inter, sans-serif] | Corpo de texto e títulos |

**Plataforma:** [ex: Web responsivo | App mobile nativo | Desktop Electron]

**Referências visuais:** [ex: "Painel principal inspirado no dashboard do Linear — densidade alta, cards com borda sutil"]

---

## Mapa de Bounded Contexts

> *Liste os contextos de domínio deste SaaS. Cada um terá seu próprio GLOSSARY.md.*
> *Consulte ARCHITECTURE.md seção 6 para regras de Bounded Contexts.*

| Bounded Context | Responsabilidade | GLOSSARY |
|---|---|---|
| [ex: `billing`] | [ex: Planos, assinaturas, faturas, pagamentos] | [ex: specs/billing/GLOSSARY.md] |
| [ex: `auth`] | [ex: Tenants, usuários, permissões, JWT] | [ex: specs/auth/GLOSSARY.md] |
| [ex: `action-plan`] | [ex: Planos de ação 5W2H, ações, responsáveis] | [ex: specs/action-plan/GLOSSARY.md] |

---

## Restrições

> *Condicionantes que afetam decisões de design — regulatórias, técnicas ou de negócio.*

**Regulatórias:**
- [ ] LGPD/GDPR aplica — dados pessoais de usuários precisam de soft delete e exportação (ver SAAS_PATTERNS.md)
- [Adicione outras regulamentações aplicáveis]

**Técnicas:**
- [ ] [ex: Deve rodar em infraestrutura existente na AWS — sem dependências de serviços GCP/Azure]
- [ ] [ex: Máximo 2s de latência em endpoints críticos com P95]

**De negócio:**
- [ ] [ex: Precisa integrar com sistema legado X via API REST — não podemos alterar o sistema legado]
- [ ] [ex: Suporte a no mínimo 3 idiomas desde o lançamento: PT-BR, EN, ES]
