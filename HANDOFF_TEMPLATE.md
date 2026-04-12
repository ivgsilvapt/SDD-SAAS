# HANDOFF.md — Snapshot de Sessão

> **Gerado automaticamente pelo `/pause-session`.**
> **Usado pelo `/resume-session` para retomar o trabalho exatamente de onde parou.**
> Sempre sobrescrito ao pausar — representa sempre o estado mais recente.

---

## Sessão Pausada em

Data/hora: [AAAA-MM-DD HH:MM]

---

## SPEC em Trabalho

Arquivo: `specs/[dominio]/[feature].md`
SPRINT atual: [N]

---

## Estado dos FRs do SPRINT [N]

| FR | Descrição resumida | Estado |
|---|---|---|
| FR-001 | [ex: Entidade Subscription criada com value objects] | ✅ Completo |
| FR-002 | [ex: Interface ISubscriptionRepository definida] | ✅ Completo |
| FR-003 | [ex: Domain Service SubscriptionCanceler — lógica de cancelamento] | 🔄 Em progresso (50%) |
| FR-004 | [ex: Domain Event SubscriptionCanceled publicado no cancelamento] | ⏳ Não iniciado |

---

## Última Ação Realizada

[ex: Criado `domain/subscription/services/SubscriptionCanceler.ts` com o método `cancel()` implementado mas sem o Domain Event ainda. O teste unitário para FR-003 está falhando — RED correto.]

---

## Próximo Passo Concreto

[ex: Completar o ciclo TDD do FR-003: adicionar `SubscriptionCanceled` domain event ao aggregate, fazer o teste passar (GREEN), depois refatorar. Em seguida iniciar FR-004.]

---

## Perguntas em Aberto

[ex: O que acontece com faturas geradas para o período após o cancelamento? Definir antes de implementar FR-004.]

---

## Contexto Adicional para a IA

> *Informações que a IA precisará ao retomar — não óbvias a partir do código.*

- [ex: A interface `ISubscriptionRepository` está em `domain/subscription/repositories/`, não em `shared/` como outros repositórios — decisão intencional registrada no STATE.md.]
- [ex: Decidimos não usar o Outbox para o SubscriptionCanceled porque ele não precisa notificar outros BCs nesta versão. Rever no SPRINT 5 quando adicionarmos notificações.]
