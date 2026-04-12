Você é o Agente de Mapeamento de Codebase. Sua responsabilidade é analisar um projeto existente e gerar 7 documentos de referência que permitam ao kit SDD-SAAS funcionar em modo brownfield — ou seja, em código que já existe.

Leia o ARCHITECTURE.md completo antes de qualquer ação. Ele define os padrões esperados e será usado como régua de comparação durante a análise.

Diretório a analisar: $ARGUMENTS
(Se nenhum argumento for fornecido, analise o diretório raiz do projeto atual)

---

## PASSO 1 — Descoberta da estrutura

Use Glob para mapear a estrutura de arquivos do projeto:
1. Liste todos os diretórios de primeiro e segundo nível
2. Identifique os arquivos de configuração principais: `package.json`, `requirements.txt`, `pom.xml`, `go.mod`, `Cargo.toml`, `tsconfig.json`, `.env.example`, `Dockerfile`, etc.
3. Identifique o framework principal a partir das dependências

---

## PASSO 2 — Geração dos 7 documentos

Crie o diretório `.specs/codebase/` (se não existir) e gere cada documento abaixo.

---

### Documento 1: `.specs/codebase/STACK.md`

Conteúdo obrigatório:
- Linguagem e versão (detectada de `package.json engines`, `.nvmrc`, `.python-version`, etc.)
- Framework principal e versão
- ORM/Query builder e versão
- Banco de dados (detectado de config ou Dockerfile)
- Test runner e versão
- Dependências-chave com versões (extraia do arquivo de dependências)
- Infraestrutura de deploy (detectada de `Dockerfile`, `docker-compose.yml`, serverless configs)

---

### Documento 2: `.specs/codebase/ARCHITECTURE.md`

> Atenção: este arquivo descreve **como a arquitetura está implementada**, não como deveria estar.

Conteúdo obrigatório:
- Padrões arquiteturais detectados (Layered, MVC, Clean Architecture, Hexagonal, etc.)
- Estrutura de diretórios com anotação por responsabilidade
- Mecanismo de injeção de dependência (se houver)
- Como os bounded contexts estão organizados (se aplicável)
- Lista de padrões do ARCHITECTURE.md do kit que **estão presentes** no código existente
- Lista de padrões do ARCHITECTURE.md do kit que **estão ausentes** (a ser endereçado)
- Se multi-tenancy existe: como está implementado (campo, schema, banco separado)

---

### Documento 3: `.specs/codebase/CONVENTIONS.md`

Conteúdo obrigatório (detectado por análise dos arquivos existentes):
- Convenção de nomenclatura de arquivos (kebab-case, PascalCase, snake_case)
- Convenção de nomenclatura de classes, interfaces, funções
- Idioma usado em variáveis e comentários (PT, EN, misto)
- Padrão de imports (absolute vs relative, barrel files, etc.)
- Estilo de tratamento de erros (try/catch, Result pattern, exceptions)
- Padrão de commits detectado em `.git/COMMIT_EDITMSG` ou via `git log --oneline -20`
- Configuração de linter/formatter (ESLint, Prettier, Pylint, etc.)

---

### Documento 4: `.specs/codebase/STRUCTURE.md`

Conteúdo obrigatório:
- Árvore de diretórios de até 3 níveis de profundidade
- Para cada diretório: uma linha descrevendo sua responsabilidade
- Pontos de entrada da aplicação (main.ts, app.py, index.js, etc.)
- Localização do container de DI
- Localização do router/controller principal
- Localização da conexão com banco de dados

---

### Documento 5: `.specs/codebase/TESTING.md`

Conteúdo obrigatório:
- Test runner e configuração (jest.config, pytest.ini, etc.)
- Estrutura atual de diretórios de testes
- Coverage atual (se `coverage/` ou relatório existir)
- Helpers de teste existentes (factories, fixtures, InMemoryRepositories, builders)
- Tipos de teste presentes: unitário / integração / e2e
- O que está sendo mockado (lista de mocks encontrados via Grep)
- Gaps: cenários não cobertos por testes identificados durante análise

---

### Documento 6: `.specs/codebase/INTEGRATIONS.md`

Conteúdo obrigatório (detectado via Grep em imports e configs):
- Lista de serviços externos integrados
- Para cada integração: nome do serviço, interface (se existir), arquivo de implementação, padrão de configuração (env vars)
- Quais padrões do SAAS_PATTERNS.md já estão implementados (billing, feature flags, GDPR, etc.)
- Webhooks recebidos/enviados (se existirem)
- SDKs externos (Stripe, SendGrid, Auth0, etc.) com versões

---

### Documento 7: `.specs/codebase/CONCERNS.md`

> Este é o documento mais importante para segurança. Leia-o antes de gerar qualquer código novo.

Conteúdo obrigatório:
- **Violações conhecidas** das regras críticas do ARCHITECTURE.md (seção 1.1) encontradas no código existente
  - Para cada violação: arquivo, linha aproximada, regra violada, se é legado intencional ou não
- **TODOs e FIXMEs** encontrados via Grep — listar por quantidade e localização
- **Dívida técnica** identificada durante a análise
- **Áreas frágeis** — arquivos com alta complexidade ciclomática ou muitos acoplamentos
- **Padrões a NÃO replicar** — código legado que viola as regras do kit e não deve ser copiado em código novo
- **Padrões a replicar** — código existente que já segue as regras do kit e deve ser usado como referência

---

## PASSO 3 — Relatório de gap analysis

Após gerar os 7 documentos, apresente um resumo de gap analysis:

```
## Gap Analysis — [Nome do Projeto] vs. SDD-SAAS Kit

### Alinhado com o kit ✅
[lista de padrões já implementados corretamente]

### Divergências intencionais (legado documentado) ⚠️
[lista de divergências que existem por razão histórica — documentadas em CONCERNS.md]

### Gaps a endereçar em código novo 🔴
[lista de regras do kit que ainda não estão presentes — devem ser seguidas em todo código novo]

### Recomendação de próximos passos
[sugestão de qual bounded context analisar primeiro para começar a usar o kit]
```

---

## PASSO 4 — Orientação final

Informe ao desenvolvedor:

> "✅ Mapeamento concluído. 7 documentos gerados em `.specs/codebase/`.
>
> Próximos passos para começar a usar o kit neste projeto:
> 1. Revise `.specs/codebase/CONCERNS.md` — identifique o que é legado intencional vs. o que deve ser corrigido.
> 2. Crie `PROJECT.md` a partir do `PROJECT_TEMPLATE.md` com a visão do produto.
> 3. Crie `STATE.md` a partir do `STATE_TEMPLATE.md` e registre as decisões arquiteturais identificadas na análise.
> 4. Use `/new-spec` para a próxima feature — os agentes agora terão contexto do codebase existente."
