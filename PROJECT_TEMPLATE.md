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
