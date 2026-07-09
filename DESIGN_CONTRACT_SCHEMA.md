# DESIGN_CONTRACT_SCHEMA.md — Schema do `design-contract.json`

O `design-contract.json` é o contrato máquina-legível que descreve a UI de uma feature: telas, navegação, ações, componentes, dados exigidos e expectativas de API. É gerado pelo Agente Design (ver `AGENTS.md`) e validado pelo Agente Design Lock antes de ser travado.

Convenções de ID: ver `TRACEABILITY_GUIDE.md`. Regra geral: **cada botão = uma ação; ações com dados apontam uma `apiExpectation`; ações puramente de UI são marcadas como UI-only.**

## Schema (exemplo em branco)

```json
{
  "version": "1.0",
  "visual": {
    "direction": "descrição da direção visual",
    "density": "dense | comfortable",
    "tokens": {
      "colors": { "bg": "#hex", "surface": "#hex", "card": "#hex", "border": "#hex", "fg": "#hex", "muted": "#hex", "accent": "#hex", "success": "#hex", "warning": "#hex", "danger": "#hex", "info": "#hex" },
      "typography": { "body": "font stack", "mono": "font stack", "display": "font + peso" },
      "spacing": { "xs": "4px", "sm": "8px", "md": "12px", "lg": "16px", "xl": "24px", "2xl": "32px" },
      "radii": { "sm": "4px", "md": "6px", "lg": "10px" }
    }
  },
  "navigation": {
    "primary": [
      { "id": "nav-slug", "label": "...", "targetScreenId": "tela", "userStoryIds": ["US-01"] }
    ]
  },
  "screens": [
    {
      "id": "tela",
      "userStoryIds": ["US-01"],
      "title": "...",
      "route": "#rota",
      "purpose": "...",
      "states": ["idle"],
      "actions": [
        { "id": "action-slug", "label": "...", "type": "submit|button|toggle|link", "userStoryIds": ["US-01"], "apiExpectationIds": ["api-slug"] }
      ],
      "dataRequirementIds": ["data-slug"]
    }
  ],
  "components": [
    { "id": "comp-slug", "name": "...", "type": "chrome|form|display|feedback|nav", "usedInScreenIds": ["tela"], "props": {}, "states": [] }
  ],
  "dataRequirements": [
    {
      "id": "data-slug",
      "name": "...",
      "description": "...",
      "fields": [ { "name": "...", "typeHint": "...", "required": true } ],
      "sourceScreenIds": ["tela"],
      "userStoryIds": ["US-01"]
    }
  ],
  "apiExpectations": [
    {
      "id": "api-slug",
      "operation": "...",
      "screenIds": ["tela"],
      "actionIds": ["action-slug"],
      "methodHint": "POST|GET|invoke",
      "requestShape": {},
      "responseShape": {},
      "userStoryIds": ["US-01"]
    }
  ],
  "deltas": [
    { "id": "delta-001", "type": "ux-decision|scope-cut|addition", "description": "...", "impact": "low|medium|high", "relatedUserStoryIds": ["US-01"], "requiresRequirementsChange": false }
  ]
}
```

## Notas

- `version` segue o schema, não o `VERSION` do kit.
- Toda action com efeito colateral (`type: submit`) deve apontar `apiExpectationIds`. Ações puramente de navegação/UI (`type: toggle` local, `type: link` interno) podem omitir `apiExpectationIds` — trate-as como UI-only.
- `deltas` registram decisões de design que desviam da SPEC original (ex: um campo do SPEC virou opcional na UI). `requiresRequirementsChange: true` sinaliza que o SPEC precisa ser atualizado — nunca decida isso silenciosamente.
- O arquivo `artifact.html` (gerado junto ao contract) deve conter todas as telas declaradas em `screens` — é uma das 13 regras do Design Lock (ver `DESIGN_LOCK_CHECKLIST.md`).
