# Guia de Mapeamento de Codebase (Brownfield)

Este guia explica como usar o kit SDD-SAAS em projetos que **já possuem código existente** (brownfield), em vez de projetos novos (greenfield).

---

## Quando usar este guia

Use este guia quando você:
- Quer aplicar o kit SDD-SAAS a um projeto que já está em produção
- Está assumindo um projeto legado e precisa de ordem no desenvolvimento
- Quer adotar as regras de Clean Architecture + DDD em código já escrito
- Precisa que os agentes entendam o que já existe antes de gerar código novo

**Não use** para projetos novos (ainda sem código) — comece diretamente pelo `PROJECT_TEMPLATE.md` e `GLOSSARY_TEMPLATE.md`.

---

## O Comando `/map-codebase`

```
/map-codebase [caminho opcional]
```

Exemplos:
```
/map-codebase                    → analisa o diretório raiz do projeto
/map-codebase src/               → analisa apenas o diretório src/
/map-codebase src/billing/       → analisa apenas o bounded context billing
```

O comando gera 7 documentos de referência em `.specs/codebase/`. Execute **uma vez** ao trazer o kit para um projeto existente. Re-execute quando a arquitetura do projeto mudar significativamente.

---

## Os 7 Documentos Gerados

### `.specs/codebase/STACK.md`
**O que contém:** versões exatas de todas as dependências-chave (framework, ORM, test runner, etc.)

**Como usar:** Inclua como contexto do Agente Implementation para que ele use as APIs corretas da versão real instalada no projeto — não a versão mais recente que conhece.

**Quando atualizar:** Após `npm install` / `pip install` com mudança de versão.

---

### `.specs/codebase/ARCHITECTURE.md`
**O que contém:** como a arquitetura está **realmente** implementada, incluindo divergências do padrão ideal do kit.

**Como usar:** Inclua como contexto do Agente Implementation (Sprint 2+) para que ele saiba como os bounded contexts existentes estão estruturados.

**Quando atualizar:** Após refatorações estruturais significativas.

---

### `.specs/codebase/CONVENTIONS.md`
**O que contém:** padrões de nomenclatura, imports, idioma do código, estilo de erro — tudo detectado do código existente.

**Como usar:** Inclua como contexto do Agente Implementation para que o código gerado siga as mesmas convenções do projeto (não invente um novo estilo).

**Quando atualizar:** Após decisão de mudar uma convenção de naming ou estilo.

---

### `.specs/codebase/STRUCTURE.md`
**O que contém:** árvore de diretórios anotada com a responsabilidade de cada pasta.

**Como usar:** Contexto rápido para qualquer agente entender onde colocar novos arquivos em projetos com estrutura diferente do padrão do kit.

**Quando atualizar:** Após criação de novos módulos ou reorganização de pastas.

---

### `.specs/codebase/TESTING.md`
**O que contém:** infraestrutura de testes atual — helpers existentes, coverage, tipos de teste presentes.

**Como usar:** Inclua como contexto do Agente Testing para que ele reutilize helpers existentes (factories, fixtures, builders) em vez de criar do zero.

**Quando atualizar:** Após criar novos helpers de teste significativos.

---

### `.specs/codebase/INTEGRATIONS.md`
**O que contém:** todos os serviços externos já integrados, com interfaces e padrões de configuração.

**Como usar:** Contexto do Agente Implementation ao trabalhar em SPRINTs de Infrastructure — evita que o agente crie uma nova integração duplicando uma existente.

**Quando atualizar:** Após integrar novo serviço externo.

---

### `.specs/codebase/CONCERNS.md`
**O que contém:** violações das regras críticas do kit que existem no código legado, TODOs/FIXMEs, áreas frágeis e padrões a não replicar.

**Como usar:** Inclua como contexto do Agente Review. O Review saberá que certas violações já existem por razão histórica — e não as aprovará como padrão para código **novo**, mas tampouco reprovará como se fossem novas violações.

**Quando atualizar:** Quando violações legadas forem corrigidas (remova a entrada) ou quando novas dívidas forem conscientemente adicionadas (documente o motivo).

> **Importante:** O CONCERNS.md documenta o que é "legado intencional". Não é uma licença para replicar esses padrões. Todo código novo deve seguir o ARCHITECTURE.md do kit — independente do que o legado faz.

---

## Como Incluir os Docs de Codebase nos Agentes

A tabela de contexto do `AGENTS.md` foi atualizada com referências aos docs de codebase. O padrão recomendado:

| Agente | Docs de codebase a incluir |
|---|---|
| Implementation Sprint 1 | `STACK.md` + `CONVENTIONS.md` |
| Implementation Sprint 2+ | `STACK.md` + `CONVENTIONS.md` + `ARCHITECTURE.md` (codebase) |
| Implementation (infra/integração) | `STACK.md` + `INTEGRATIONS.md` + `CONVENTIONS.md` |
| Testing | `TESTING.md` |
| Review | `CONCERNS.md` (para distinguir legado de nova violação) |
| Migration | `STACK.md` (para versão correta do ORM/banco) |

---

## Processo Completo para Adotar o Kit em Projeto Existente

```
1. Execute /map-codebase
       ↓ gera .specs/codebase/ com os 7 documentos
2. Revise CONCERNS.md
       ↓ identifique: o que é legado intencional vs. o que deve ser corrigido
3. Crie PROJECT.md (copie PROJECT_TEMPLATE.md)
       ↓ documente a visão do produto
4. Crie STATE.md (copie STATE_TEMPLATE.md)
       ↓ registre as decisões arquiteturais identificadas na análise
5. Crie GLOSSARY.md para o bounded context principal (copie GLOSSARY_TEMPLATE.md)
       ↓ documente a Ubiquitous Language do domínio
6. Use /new-spec para a próxima feature
       ↓ a partir daqui, o fluxo normal de 6 agentes se aplica
```

---

## Perguntas Frequentes

**O mapeamento muda o código existente?**
Não. O `/map-codebase` é somente leitura — analisa e documenta, sem modificar nenhum arquivo do projeto.

**Preciso corrigir todas as violações do CONCERNS.md antes de começar?**
Não. O CONCERNS.md documenta o estado atual para que agentes futuros saibam o que é legado. O objetivo é: não replicar as violações em código novo, e corrigi-las gradualmente quando houver oportunidade (via SPRINT de refatoração com SPEC próprio).

**Posso rodar `/map-codebase` em partes do projeto?**
Sim. Se o projeto for grande, rode por bounded context: `/map-codebase src/billing/`. Os docs gerados serão parciais mas úteis para o contexto daquele bounded context.

**O que fazer quando o STACK.md fica desatualizado?**
Rode `/map-codebase` novamente, ou edite manualmente o `STACK.md` para refletir a nova versão da dependência.
