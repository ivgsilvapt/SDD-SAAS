## Contexto

<!-- Por que esta mudança é necessária? Qual problema resolve? -->

## SPEC relacionada

<!-- Link para a SPEC aprovada em specs/ (obrigatório para features e refactors) -->
- SPEC: `specs/[bounded-context]/SPEC-[slug].md`

## Tipo de mudança

- [ ] Feature (nova funcionalidade — requer SPEC aprovada)
- [ ] Fix (correção de bug — pode usar `/quick-fix` se ≤3 arquivos)
- [ ] Refactor (sem mudança de comportamento)
- [ ] Docs / Config
- [ ] CI/CD

## Checklist SDD-SAAS

### Arquitetura
- [ ] Não viola regras de dependência de camadas (Domain ← Application ← Infrastructure ← Presentation)
- [ ] Toda entidade nova tem `tenantId` obrigatório
- [ ] Todo repositório novo filtra por `tenantId` em todas as queries
- [ ] Nenhum import de camada superior para inferior (ex: Domain não importa Application)

### Qualidade
- [ ] Testes unitários passando (`npm run test:unit` ou `pytest`)
- [ ] Testes de integração passando (se aplicável)
- [ ] TypeScript sem erros (`npm run typecheck` ou `mypy`)
- [ ] Lint sem warnings (`npm run lint` ou `ruff check`)

### Segurança
- [ ] Sem secrets, tokens ou URLs de produção no código
- [ ] Inputs do usuário validados em `Presentation`
- [ ] Sem SQL injection (use ORM/query builder parametrizado)

### Documentação
- [ ] `STATE.md` atualizado se houver decisão arquitetural não-óbvia
- [ ] `GLOSSARY.md` atualizado se novos termos de domínio foram introduzidos
- [ ] SPEC marcada como implementada (se feature completa)

## Como testar

<!-- Passos para o revisor verificar manualmente -->
1. 
2. 
3. 

## Screenshots (se UI)

<!-- Adicione screenshots para mudanças visuais -->
