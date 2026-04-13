---
name: phase-guards
description: What GSD2 agents should and should not do during each phase of execution, from the perspective of Clean Architecture + DDD.
---

# Phase Guards — Clean Architecture in GSD2 Context

Phase guards are scope guidelines for GSD2 agents. They are not execution gates — GSD2 remains autonomous. They define what good judgment looks like for each phase.

---

## Discussion / Planning Phase (`M###-CONTEXT.md`, `S##-PLAN.md`)

**SHOULD:**
- Read `ARCHITECTURE.md` before planning any implementation
- Read `docs/[context]/GLOSSARY.md` to use canonical domain terms in plans
- Identify which layer each planned component belongs to
- Name Domain objects (Entity, VO, Aggregate) before naming infrastructure
- Record new architectural decisions in `.gsd/DECISIONS.md` during planning
- Ask: "Does this feature introduce a new domain concept? If yes, model the domain first."
- Plan Domain and Application layers before Infrastructure and Presentation

**SHOULD NOT:**
- Plan infrastructure (DB schema, HTTP routes) without first modeling the domain
- Use ORM-specific terms (table, column, query) inside domain-layer planning
- Create Use Cases that bypass the Repository interface (direct DB calls)
- Name things that contradict `GLOSSARY.md` terms

---

## Implementation Phase (task execution)

**SHOULD:**
- Start with Domain layer files before other layers
- Create Repository interface in `domain/` before creating ORM implementation in `infrastructure/`
- Implement invariants as throwing constructors or factory methods on Entities
- Keep Use Cases thin: load via Repository → call domain method → save → return DTO
- Record a DECISIONS.md entry when making a non-obvious architectural choice
- Add entry to `.gsd/KNOWLEDGE.md` when a pattern proves useful or fails

**SHOULD NOT:**
- Import `infrastructure/` from `domain/` — NEVER
- Import `application/` from `domain/` — NEVER
- Put business logic in a Controller
- Put business logic in an ORM model or DB adapter
- Create a Use Case that calls another Use Case (use Application Service instead)
- Create Repository interface in `infrastructure/` (it belongs in `domain/`)
- Introduce a new third-party library without recording the decision in DECISIONS.md
- Skip creating Domain Events for state changes that downstream contexts will care about

---

## Testing Phase

**SHOULD:**
- Test domain objects with pure unit tests — no mocks needed (domain has no dependencies)
- Test Use Cases with Repository mocked — inject a fake or in-memory implementation
- Test Infrastructure (repository implementations) with a real database (test container or in-memory)
- Test Presentation (controllers) with the full HTTP stack running

**SHOULD NOT:**
- Mock the database to test infrastructure — defeats the purpose of integration tests
- Test domain logic through HTTP endpoints — test it directly via unit tests
- Modify production code to make testing easier (if you feel the urge, it's a design smell)

---

## Review / Verification Phase

**SHOULD:**
- Verify imports: no `infrastructure/` in `domain/`, no `infrastructure/` in `application/`
- Verify layer placement: entities in `domain/`, controllers in `presentation/`
- Verify Repository interfaces are in `domain/`, implementations in `infrastructure/`
- Check for anemic domain: entities with only getters/setters and no behavior → flag as advisory
- Use `arch-guide review` skill to produce a formal report if violations are suspected

**SHOULD NOT:**
- Approve a slice where `domain/` imports from `infrastructure/` — critical violation blocks shipping
- Apply architecture fixes directly during review — create a fix task instead

---

## Cross-Cutting: Always Valid

These apply in every phase:

1. **Use GLOSSARY.md terminology.** If a term isn't in the glossary, add it before using it in code.
2. **Dependency direction is sacred.** Inner layers do not depend on outer layers. Ever.
3. **Record decisions.** Non-obvious architectural choices go to `.gsd/DECISIONS.md`.
4. **Record lessons.** Recurring patterns or anti-patterns go to `.gsd/KNOWLEDGE.md`.
5. **Domain first.** When in doubt about ordering, model the domain before writing infrastructure.
