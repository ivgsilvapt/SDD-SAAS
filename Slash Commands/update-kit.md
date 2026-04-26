# /update-kit

Atualiza os arquivos de referência do SDD-SAAS Kit em um projeto existente, comparando
com a versão mais recente do kit-fonte e aplicando apenas as mudanças aprovadas.

**Uso:** `/update-kit /caminho/para/o/kit`

---

## PASSO 1 — Verificar pré-requisitos

1. Verifique que `$ARGUMENTS` foi fornecido com o caminho para o diretório do kit-fonte.
   - Se não foi fornecido: informe `"Uso: /update-kit /caminho/para/o/sdd-saas-kit"` e encerre.
2. Verifique que o diretório do kit-fonte existe e contém `ARCHITECTURE.md`.
   - Se não existe: informe `"Caminho do kit-fonte inválido: [caminho] não encontrado."` e encerre.
3. Leia o arquivo `VERSION` do kit-fonte (se existir) e registre como `[versao-nova]`.
4. Leia o arquivo `VERSION` do projeto atual (se existir) e registre como `[versao-atual]`.
5. Exiba:

```
Atualizando para kit v[versao-nova] (atual: v[versao-atual])
Kit-fonte: [caminho-do-kit]
Projeto: [diretório atual]
```

---

## PASSO 2 — Definir arquivos de referência

Os arquivos abaixo são cópias diretas do kit. Ao contrário de ARCHITECTURE.md, eles
**não devem conter customizações locais** — podem ser substituídos com segurança.

Lista de arquivos de referência:
```
AGENTS.md
SPEC_TEMPLATE.md
TESTING_GUIDE.md
SAAS_PATTERNS.md
GLOSSARY_TEMPLATE.md
GIT_WORKFLOW.md
KNOWLEDGE_TEMPLATE.md
DISCOVERY_TEMPLATE.md
HANDOFF_TEMPLATE.md
STATE_TEMPLATE.md
CODEBASE_MAPPING_GUIDE.md
PROJECT_TEMPLATE.md
ROADMAP_TEMPLATE.md
CHANGELOG.md
VERSION
```

Arquivo tratado separadamente (pode conter customizações locais): `ARCHITECTURE.md`

---

## PASSO 3 — Comparar arquivos de referência

Para cada arquivo da lista do PASSO 2:

1. Verifique se existe no diretório do kit-fonte.
2. Verifique se existe no projeto atual.
3. Se existe em ambos: compare o conteúdo. Se diferente, classifique como `DESATUALIZADO`.
4. Classifique como `NOVO` se não existe no projeto mas existe no kit-fonte.
5. Classifique como `ATUALIZADO` se o conteúdo for idêntico.
6. Classifique como `APENAS LOCAL` se existe no projeto mas não no kit-fonte (ignorar).

Repita para `ARCHITECTURE.md` — registre o resultado separadamente.

---

## PASSO 4 — Comparar slash commands

1. Liste todos os arquivos `.md` em `[kit-fonte]/Slash Commands/` (exceto `CLAUDE.md`).
2. Compare com os arquivos em `.claude/commands/` do projeto atual.
3. Classifique cada comando como `NOVO`, `DESATUALIZADO` ou `ATUALIZADO`.

---

## PASSO 5 — Apresentar relatório e aguardar confirmação

Exiba o relatório completo:

```
============================================================
Relatório de Atualização do Kit
============================================================

Arquivos de referência:
  ATUALIZADO  | AGENTS.md
  DESATUALIZADO | SPEC_TEMPLATE.md
  NOVO        | DISCOVERY_TEMPLATE.md
  ...

Slash commands (.claude/commands/):
  NOVO        | discover.md
  DESATUALIZADO | impl-sprint.md
  ...

ARCHITECTURE.md:
  Status: DESATUALIZADO
  Atenção: este arquivo pode conter customizações locais.
  O diff será exibido antes da substituição.

Resumo: [N] arquivos desatualizados, [M] novos, [K] inalterados.
============================================================

Deseja prosseguir com a atualização? (responda s para continuar)
```

Aguarde a resposta antes de prosseguir. Se a resposta não for `s` ou `sim`, encerre com:
`"Atualização cancelada. Nenhum arquivo foi modificado."`

---

## PASSO 6 — Executar atualizações

**6a. Arquivos de referência (exceto ARCHITECTURE.md):**
Para cada arquivo classificado como `DESATUALIZADO` ou `NOVO`:
- Copie o arquivo do kit-fonte para o diretório atual.
- Registre: `"Atualizado: [nome-do-arquivo]"`

**6b. Slash commands:**
Para cada comando classificado como `DESATUALIZADO` ou `NOVO`:
- Copie o arquivo do kit-fonte para `.claude/commands/`.
- Registre: `"Atualizado: .claude/commands/[nome].md"`

**6c. ARCHITECTURE.md (se desatualizado):**
1. Exiba um resumo das diferenças entre a versão do kit e a versão local, seção por seção.
   Use o formato:
   ```
   Seção [N] — [título]: [adicionada / modificada / inalterada]
   ```
2. Pergunte: `"Deseja substituir ARCHITECTURE.md pela versão do kit? (s = substituir / n = manter local / d = mostrar diff completo)"`
3. Se `s`: substitua o arquivo.
4. Se `n`: mantenha a versão local e registre: `"ARCHITECTURE.md mantido (revisão manual necessária)."`
5. Se `d`: exiba o diff completo e repita a pergunta.

---

## PASSO 7 — Confirmar e registrar

1. Exiba a lista de todos os arquivos atualizados.
2. Se existir `STATE.md` no projeto, adicione à Seção 4 (Log de Sessão):
   ```
   [data atual] — Kit atualizado: v[versao-atual] -> v[versao-nova]
   Arquivos atualizados: [lista separada por vírgulas]
   ```
3. Exiba a mensagem final:

```
============================================================
Kit atualizado para v[versao-nova].
[N] arquivos de referencia atualizados.
[M] slash commands atualizados/adicionados.
[mensagem sobre ARCHITECTURE.md se aplicável]

Proximos passos recomendados:
1. Leia CHANGELOG.md para ver o que mudou nesta versao.
2. Revise ARCHITECTURE.md se manteve a versao local.
3. Execute: python Scripts/validate-kit.py (se disponivel)
============================================================
```
