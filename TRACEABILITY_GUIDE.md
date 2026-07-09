# TRACEABILITY_GUIDE.md — Convenções de ID e Rastreabilidade de Especificação

Este guia define as convenções de ID usadas em SPECs, no design travado (`design-contract.json` — ver `DESIGN_CONTRACT_SCHEMA.md`) e em sprints. Objetivo: toda decisão de produto é rastreável de ponta a ponta — de uma User Story até a tabela de banco que a implementa.

---

## Convenções de ID

| Artefato | Formato | Onde vive | Nível Markdown |
|---|---|---|---|
| User Story | `US-01`, `US-02`... | SPEC_TEMPLATE.md, seção "User Stories" | `####` |
| Requisito Funcional | `FR-01`... (o kit usa `FR`, não `RF`) | SPEC_TEMPLATE.md, seção "Requisitos Funcionais" — sempre com coluna "User Story" | tabela |
| Requisito Não-Funcional | `NFR-01`... | SPEC_TEMPLATE.md, seção "Requisitos Não-Funcionais" — sempre com "Critério de Aceitação" | tabela |
| Tela | `tela-slug` (ex: `dashboard`, `action-plans-list`) | seção "Impacto em UX" do SPEC, ou `design-contract.json` | — |
| Navegação | `nav-slug` | `design-contract.json` | — |
| Ação | `action-slug` (ex: `create-action-plan`) | seção "Impacto em UX" do SPEC, ou `design-contract.json` | — |
| Componente | `comp-slug` | `design-contract.json` | — |
| Dado exigido | `data-slug` | `design-contract.json` | — |
| Expectativa de API | `api-slug` | `design-contract.json` | — |
| Delta de design | `delta-001`... | `design-contract.json` | — |
| Feature de sprint | `feat-xx-yy` (xx=sprint, yy=sequência) | `sprints.json` (quando existir planejamento macro) | — |

## Cadeia de Rastreabilidade Obrigatória

```
US → FR/NFR → tela → ação → apiExpectation → tabela (banco)
```

Quando o SPEC afeta a camada Presentation, a seção "Impacto em UX" do SPEC deve referenciar os IDs de tela e ação envolvidos — não é obrigatório usar `design-contract.json` para toda feature, apenas quando o Agente Design Lock estiver em uso (ver `DESIGN_CONTRACT_SCHEMA.md`).

## Regra de Imutabilidade

IDs nunca são renumerados nem reaproveitados. Ao adicionar um novo item, continue a sequência existente — nunca reordene os já existentes, mesmo que a numeração pareça fora de ordem depois de remoções.

## Tabela de Rastreabilidade Padrão (modelo)

Use este modelo ao final de um SPEC quando `design-contract.json` estiver travado para a feature:

| US | FR | Tela | API | Tabela |
|---|---|---|---|---|
| US-01 | FR-01 | dashboard | list-invoices | invoices |
