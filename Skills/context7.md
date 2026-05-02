---
name: context7
description: Busca documentação oficial e versionada de bibliotecas externas via Context7 (Upstash). Use quando precisar de API atual de NestJS, Pydantic, Prisma, Next.js, Supabase ou qualquer lib cuja versão pode ter mudado após o cutoff de treinamento. NÃO use para padrões internos do projeto.
version: 1.0.0
---

# Context7 — Documentação de bibliotecas sempre atualizada

Skill que conecta o agente ao [Context7 (Upstash)](https://github.com/upstash/context7) — fonte de **documentação versionada e atualizada** de bibliotecas open-source. Resolve o problema de modelos LLM gerarem código contra APIs antigas (cutoff de treinamento) ou alucinarem métodos que não existem mais.

## Quando usar

- A API de uma lib externa parece ter mudado (NestJS v11, Pydantic v2, Prisma v6, Next.js App Router, Supabase Auth v2, etc.)
- Erro de import/typing inesperado em lib externa
- Usuário pede explicitamente: "use context7", "consulta Context7", "docs atualizados de X"
- Antes de codar contra uma lib que tem releases frequentes

## Como invocar

1. **Modo prompt (recomendado):** inclua `use context7` no prompt antes de codar contra a lib externa. Exemplo: *"Implemente um interceptor de NestJS que loga latência de requests. use context7"*.
2. **Modo CLI on-demand:** `npx -y @upstash/context7-mcp` via Bash quando precisar de uma consulta pontual fora do contexto MCP.
3. **Modo MCP (opt-in):** se o projeto adotou MCP via `.mcp.json` (ver `ORIENTACAO.md` §2.7), o servidor Context7 já estará disponível como tool nativa em todas as sessões.

## Quando NÃO usar

- Padrões de arquitetura do projeto → consulte `ARCHITECTURE.md` / `SAAS_PATTERNS.md`
- Decisões internas registradas → consulte `STATE.md` / `KNOWLEDGE.md`
- Código próprio do projeto → leia `src/` direto
- Libs estáveis e bem conhecidas (lodash, dayjs, datetime nativo) — economize tokens

## Por que Skill por default e não MCP

A Skill é carregada apenas quando invocada (descoberta por nome+descrição). O MCP injetaria o schema do tool em todo system prompt, gastando tokens **mesmo em turnos que não consultam docs**. Para uso ocasional, Skill é dramaticamente mais econômica. Quem usar Context7 intensivamente pode optar pelo modo MCP — ver `harness/templates/mcp/.mcp.json` e `ORIENTACAO.md` §2.7.

## Modo HTTP + API key (rate limit maior)

Para uso intensivo, edite o `.mcp.json` do projeto para apontar para `https://mcp.context7.com/mcp` e exporte `CONTEXT7_API_KEY` (obtido em https://context7.com/dashboard). Esse modo dá rate limits maiores que o stdio.
