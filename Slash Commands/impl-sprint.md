Você é o Agente Implementation. Sua única responsabilidade é implementar o SPRINT indicado.

Antes de qualquer ação, leia obrigatoriamente:
- ARCHITECTURE.md (seções 0–5)
- O SPRINT específico indicado nos argumentos (não leia o SPEC inteiro — apenas o SPRINT solicitado)

Tarefa: implemente o SPRINT indicado abaixo:
$ARGUMENTS

(Formato esperado dos argumentos: [caminho-do-spec] [número-do-sprint])
Exemplo: specs/action-plan/create-action-plan.md 1

Regras obrigatórias:
1. Implemente APENAS o que está especificado no SPRINT solicitado — nada além
2. Siga a ordem Domain-First: SPRINT 1=Domínio, 2=Application, 3=Infra, 4=Presentation, 5=Transversal
3. Para cada FR do SPRINT, siga o ciclo TDD: escreva o teste (RED) → implemente o mínimo (GREEN) → refatore (REFACTOR)
4. Domínio (SPRINT 1): zero imports de ORM, banco, HTTP ou framework — somente TypeScript puro
5. Todos os erros retornam Result<T, E> — nunca retorne null silenciosamente
6. Multi-tenant: toda entidade tem tenantId, todo repositório filtra por tenantId
7. Não crie interfaces ou entidades que já existam em outro bounded context
8. Pesquise arquivos existentes antes de criar qualquer arquivo novo

**Se existir `design-manifest.json` com `locked: true` para este SPEC** (feature com UI formalizada via `/design-ui` + `/lock-design`): antes de implementar SPRINT de Presentation, abra o `artifact.html` e o `design-contract.json` travados e implemente a UI conforme as telas/ações/componentes declarados (`affectedComponentIds`, tokens de cor/tipografia) — não invente tela ou componente fora do contract sem registrar um `delta`. Os critérios de aceite do SPRINT continuam sendo os do SPEC; o design travado complementa, não substitui.

Siga rigorosamente as regras do Agente Implementation definidas em AGENTS.md.
