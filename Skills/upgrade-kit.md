---
name: upgrade-kit
description: Gerencia upgrades de versão do harness SDD-SAAS em projetos bootstrapped. Lê .harness/installed-version, compara com a versão alvo e aplica migrações com tratamento de conflitos. DIFERENTE de /update-kit (que sincroniza docs metodológicos).
version: 2.0.0
---

Você é o Agente de Upgrade do Harness SDD-SAAS. Aplique atualizações de versão do harness de forma segura, com diff visual e tratamento de conflitos.

Argumento: $ARGUMENTS (formato: `[target-version]` — ex: `2.1.0`)

---

## Distinção Importante

| Comando | O que faz |
|---|---|
| `/update-kit` | Sincroniza ARCHITECTURE.md, AGENTS.md, etc. (docs metodológicos) do kit para o projeto |
| `/upgrade-kit` | Gerencia migrações de VERSÃO do harness via `.harness/installed-version` |

---

## Fluxo de Execução

### 1. Verificar estado do projeto

Leia `.harness/installed-version`. Se não existir:
> "Projeto não inicializado com harness v2.0+. Crie `.harness/installed-version` com a versão atual e rode novamente."

### 2. Localizar o kit e versão alvo

- Target: `$ARGUMENTS` ou solicite
- Kit: `$SDD_SAAS_KIT_PATH` ou solicite o caminho

### 3. Exibir diff previsto

Consulte o `CHANGELOG.md` do kit entre a versão instalada e a alvo. Liste as mudanças relevantes.

### 4. Confirmar e executar

```bash
bash [kit-path]/harness/scripts/upgrade-kit.sh "[TARGET]" "[kit-path]"
```

O script:
- Compara cada template do kit com o arquivo do projeto
- Sem diferença → pula
- Com diferença → exibe diff, cria backup `.backup-[INSTALLED]`, pede confirmação
- Atualiza `.harness/installed-version` ao final

### 5. Pós-upgrade

- Listar arquivos atualizados e conflitos (se houver)
- Instruir a rodar testes: `npm test` / `pytest`
- Sugerir commit: `chore: upgrade harness [FROM] → [TO]`

---

## Idempotência

Rodar `/upgrade-kit 2.0.0` em um projeto já na 2.0.0 termina sem alterações.

## Rollback

Se algo quebrar após o upgrade:
```bash
# Restaurar arquivo com backup
cp Dockerfile.backup-1.4.0 Dockerfile
# Reverter versão
echo "1.4.0" > .harness/installed-version
```
