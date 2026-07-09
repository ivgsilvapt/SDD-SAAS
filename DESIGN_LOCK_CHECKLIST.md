# DESIGN_LOCK_CHECKLIST.md — As 13 Regras do Design Lock

Todas as 13 regras devem ser PASS para o design ser travado (`design-manifest.json` com `locked: true`). Resultado binário por regra — nunca trave com uma regra pendente.

As regras 1–6, 8, 9, 11 e 12 são **verificáveis programaticamente** (integridade referencial do JSON) — use `Scripts/validate-design-lock.py` em vez de julgamento humano/LLM para essas. As regras 7, 10 e 13 exigem julgamento e permanecem com o Agente Design Lock.

| # | Regra | Verificável por script? |
|---|---|---|
| 1 | Toda US (do SPEC) tem ≥1 tela que a cobre | Sim |
| 2 | Toda tela referencia `userStoryIds` existentes | Sim |
| 3 | Toda `action` aponta `apiExpectationIds` válidos ou é marcada UI-only | Sim |
| 4 | Toda `apiExpectation` referencia `screenIds` e `actionIds` existentes | Sim |
| 5 | Todo `dataRequirement` referencia telas-fonte (`sourceScreenIds`) existentes | Sim |
| 6 | Itens de `navigation` apontam `targetScreenId` existentes | Sim |
| 7 | Tokens de cor cobrem a identidade visual do `PROJECT.md` (seção Identidade Visual) | Não — julgamento |
| 8 | Toda tela tem ao menos o estado `"idle"` | Sim |
| 9 | Componentes listam as telas onde são usados (`usedInScreenIds` não vazio) | Sim |
| 10 | Deltas com `requiresRequirementsChange: true` foram sinalizados ao desenvolvedor | Não — julgamento |
| 11 | Nenhuma US sem cobertura de tela (gap zero) | Sim |
| 12 | IDs únicos em `screens`, `components`, `apiExpectations`, `dataRequirements` | Sim |
| 13 | `artifact.html` contém todas as telas declaradas em `screens` | Não — julgamento (inspeção do HTML) |

## Saídas do Design Lock

- **`DESIGN_LOCK_REPORT.md`** — Status `APROVADO` / `REPROVADO` + tabela PASS/FAIL das 13 regras + detalhe de cada falha (regra, ID afetado, ação de correção).
- **`design-manifest.json`** (apenas se APROVADO):
  ```json
  {
    "locked": true,
    "lockedAt": "2026-07-09T12:00:00Z",
    "htmlSha256": "...",
    "contractSha256": "..."
  }
  ```

## Calculando os hashes

```bash
# Linux/Mac
sha256sum artifact.html
sha256sum design-contract.json
```

```powershell
# Windows
certutil -hashfile artifact.html SHA256
certutil -hashfile design-contract.json SHA256
```

## Regras de Processo

- Nunca trave (`locked: true`) com qualquer regra em FAIL.
- REPROVADO volta ao Agente Design — nunca corrija o contract diretamente no Design Lock.
- Após travado, qualquer mudança no `artifact.html` ou `design-contract.json` invalida o manifest — rode `/lock-design` novamente (o hash não vai bater com o manifest antigo).
