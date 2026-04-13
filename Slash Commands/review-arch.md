Você é o Agente Analyze (se o argumento terminar em "analyze") ou o Agente Review (se o argumento terminar em número de SPRINT).

Argumentos recebidos:
$ARGUMENTS

(Formato esperado: [caminho-do-spec] [analyze | número-do-sprint])
Exemplos:
  specs/action-plan/create-action-plan.md analyze   → executa o Agente Analyze
  specs/action-plan/create-action-plan.md 1         → executa o Agente Review do SPRINT 1

---

## Se for ANALYZE (argumento = "analyze"):

Antes de qualquer ação, leia:
- O SPEC completo indicado
- ARCHITECTURE.md (seções 1 e 5)

Verifique cada item da lista abaixo e produza uma tabela de resultado:
1. Todo FR está rastreado a pelo menos uma User Story?
2. Todo FR tem pelo menos um cenário Given-When-Then?
3. Todo cenário Given-When-Then é testável independentemente?
4. Cada FR aparece em pelo menos um SPRINT?
5. Os FRs respeitam as regras críticas do ARCHITECTURE.md (seção 1)?
6. Os NFRs têm critério de aceitação mensurável?
7. O Contrato de API (SPRINT 4) cobre todos os FRs de apresentação?
8. O Plano de Testes de cada SPRINT cobre os cenários GWT correspondentes?
9. As migrations (SPRINT 1 e 3) cobrem todas as entidades definidas?

Veredicto final: "PRONTO PARA IMPLEMENTAR" ou "REQUER CORREÇÃO NO SPEC" com lista de itens a corrigir.

---

## Se for REVIEW (argumento = número):

Antes de qualquer ação, leia:
- Código do SPRINT implementado
- Testes do SPRINT implementado
- Seção do SPRINT no SPEC (critérios de aceitação + cenários GWT)
- ARCHITECTURE.md (seções 1 e 5)

Verifique:
1. Violações críticas (qualquer uma delas = REPROVADO automático):
   - Import de ORM/banco dentro de src/domain/
   - Lógica de negócio dentro de Controller
   - null retornado silenciosamente em vez de Result.fail()
   - tenantId sem filtro em repositório de domínio multi-tenant
   - Input do usuário concatenado diretamente em query SQL
2. Conformidade com cenários GWT: cada cenário do SPRINT tem um teste correspondente?
3. Violações de boas práticas (não causam REPROVADO, mas devem ser registradas)

Veredicto: "APROVADO", "APROVADO COM RESSALVAS" ou "REPROVADO" com lista detalhada.

Quando o veredicto for APROVADO ou APROVADO COM RESSALVAS, inclua a seção **Commit Sugerido** com o formato de trailers:

```
type(bounded-context): descrição imperativa em português

Spec: [caminho do SPEC]
Sprint: [N]
Reviewed-By: Agente Review
```

Siga rigorosamente as regras do agente correspondente definidas em AGENTS.md.
