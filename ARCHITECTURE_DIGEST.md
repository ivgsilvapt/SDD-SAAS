# ARCHITECTURE_DIGEST.md

> Resumo de contexto de sessão. Contém apenas as regras inegociáveis do `ARCHITECTURE.md` completo — nunca cria regra nova. Se uma regra não está aqui, não assuma que não existe: consulte a seção específica do `ARCHITECTURE.md` listada em `AGENTS.md` ("Contexto Mínimo por Agente") para o seu papel.
>
> **Exceção:** os agentes **Analyze** e **Review** sempre leem as seções completas do `ARCHITECTURE.md` (1 e 5) — nunca substituem por este digest, pois são os validadores da arquitetura.

---

## Regra SDD

Nenhuma funcionalidade nova é implementada sem SPEC aprovado em `specs/[domínio]/[feature].md`. Sem SPEC correspondente: pare e use `/new-spec` (ou `/quick-fix` se elegível — ver ARCHITECTURE.md §17).

## Ordem de Implementação (Domain-First)

Sempre de dentro para fora: **1. Domínio → 2. Application → 3. Infraestrutura → 4. Apresentação → 5. Aspectos Transversais.** Nunca comece pela UI ou pelo banco. Se não conseguir modelar o domínio, não gere código — discuta o modelo antes. (Detalhe completo: ARCHITECTURE.md §3)

## Regras Críticas — nunca viole (ARCHITECTURE.md §1.1)

- **Camadas:** nunca importe ORM/HTTP client/banco dentro de domínio ou use cases; nunca coloque lógica de negócio em Controller/View/ViewModel; presentation nunca acessa infraestrutura direto, sempre via use case.
- **Injeção de dependência:** nunca instancie dependências externas com `new` em serviços/use cases/domínio — receba via DI; dependa de interfaces, nunca de implementações concretas.
- **Transações:** abra e feche apenas na Application (Use Cases) — nunca no Controller, nunca no Domínio.
- **Configuração:** nunca hardcode valores de config — use variáveis de ambiente; nunca guarde estado entre requisições em variável de processo.
- **Erros:** nunca retorne `null` silenciosamente — use `Result<T,E>` ou exceção tipada; nunca silencie catch vazio; nunca exponha stack trace ao cliente.
- **i18n:** nunca texto literal visível ao usuário em views — sempre chave de tradução.
- **Multi-tenancy:** nunca acesse dado sem filtrar por `tenantId`; nunca passe `tenantId` como parâmetro — injete via `TenantContext`; nunca em variável global/singleton.
- **Segurança:** nunca confie em input sem validar no Command Object (Fail Fast na borda); sempre verifique autorização por tenant/recurso; nunca concatene input em query — use parâmetros.
- **Escopo:** nunca implemente além do que foi pedido na tarefa atual (YAGNI).

## Hierarquia de Desempate (ARCHITECTURE.md §17)

Quando princípios colidem, nesta ordem:
1. **Segurança e isolamento de dados** — nunca sacrificados
2. **Fail Fast** — erros sinalizados imediatamente
3. **YAGNI > OCP** — não crie extensibilidade sem requisito conhecido
4. **Isolamento de Bounded Context > DRY** — entre BCs, duplicar é preferível a acoplar
5. **KISS** — a solução mais simples que atende o requisito vence

Resoluções de conflito nomeadas (TDD vs YAGNI, Fail Fast vs Resilience, KISS vs Clean Architecture/Trivial Path, Multi-Model Routing) estão em ARCHITECTURE.md §17 — consulte a seção completa antes de aplicar uma exceção.

## Conventional Commits (ARCHITECTURE.md §20)

```
type(scope): descrição [spec-ref]
```
Tipos: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`, `ci`. Trailers recomendados: `Spec:`, `Sprint:`, `Reviewed-By:`. Nunca commite SPRINT com veredicto `REPROVADO`.

## Estrutura de Pastas (visão mínima)

```
src/{presentation,application,domain,infrastructure,shared,config}/  tests/{unit,integration,e2e}/
```
A seta de dependência aponta sempre para dentro (Presentation → Application → Domain ← Infrastructure). Árvore completa: ARCHITECTURE.md §2.
