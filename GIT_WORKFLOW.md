# GIT_WORKFLOW.md — Estratégia de Branches por SPEC

> Leia este documento uma vez durante a inicialização do projeto.
> Os agentes SDD-SAAS não enforçam git — esta é documentação de referência para o desenvolvedor.

---

## 1. Branches por SPEC

### Convenção de nomenclatura

```
spec/<slug>
```

Onde `<slug>` é o nome do arquivo SPEC sem extensão e sem o caminho de diretório.

**Exemplos:**
```
spec/billing-create-subscription
spec/auth-reset-password
spec/tenant-invite-member
spec/action-plan-create-action
```

### Regras

- **Um branch por SPEC** — todos os SPRINTs da mesma SPEC vivem no mesmo branch
- Crie o branch no momento em que o SPEC for aprovado pelo humano (antes do `/impl-sprint 1`)
- Faça commits no branch conforme cada SPRINT for aprovado pelo Agente Review
- Merge para `main` (ou branch de integração) somente após o Checklist Final da SPEC estar completo e todos os SPRINTs com veredicto APROVADO
- Prefira `git merge --no-ff` para preservar a história do branch

### Ciclo de vida do branch

```
main
  │
  ├── spec/billing-create-subscription   ← branch criado após SPEC aprovado
  │     ├── commit: feat(billing): sprint 1 — domínio
  │     │           Spec: specs/billing/create-subscription.md
  │     │           Sprint: 1  Reviewed-By: Agente Review
  │     ├── commit: feat(billing): sprint 2 — application
  │     │           Spec: specs/billing/create-subscription.md
  │     │           Sprint: 2  Reviewed-By: Agente Review
  │     ├── commit: feat(billing): sprint 3 — infraestrutura
  │     └── merge → main  (após todos os SPRINTs APROVADOS)
  │
  └── spec/auth-reset-password            ← branch paralelo, completamente isolado
```

### Comandos de referência

```bash
# Criar branch ao aprovar o SPEC
git checkout -b spec/billing-create-subscription

# Commitar SPRINT aprovado (com trailers — ver ARCHITECTURE.md seção 20)
git commit -m "feat(billing): implementa domínio de assinatura" \
           -m "Spec: specs/billing/create-subscription.md" \
           -m "Sprint: 1" \
           -m "Reviewed-By: Agente Review"

# Merge ao main após Checklist Final
git checkout main
git merge --no-ff spec/billing-create-subscription
```

---

## 2. Worktrees — Trabalho Paralelo em Duas SPECs (Avançado)

Use worktrees quando precisar alternar entre duas SPECs ativas sem stash ou perda de contexto.

```bash
# Criar worktree para uma segunda SPEC em um diretório paralelo
git worktree add ../projeto-spec-auth-reset spec/auth-reset-password

# Trabalhar na segunda SPEC no diretório isolado
cd ../projeto-spec-auth-reset
# ... execute /impl-sprint, /review-arch, etc. aqui

# Após merge, remover o worktree
git worktree remove ../projeto-spec-auth-reset
```

**Quando usar:**
- Você tem duas SPECs em andamento e precisa alternar frequentemente entre elas
- Uma SPEC está bloqueada aguardando clarificação e você quer avançar em outra

**Quando NÃO usar:**
- Quando uma SPEC depende de outra (respeite a ordem de dependência)
- Quando as SPECs compartilham os mesmos arquivos de domínio (risco de conflito)

---

## 3. Correções via `/quick-fix`

Correções que passam pelo `/quick-fix` **não usam branches `spec/`**.

- Vão direto para `main` se forem triviais (1–2 arquivos, solo developer)
- Usam `fix/<descrição-curta>` se a correção for mais complexa ou se coordenar com time

```bash
git checkout -b fix/jwt-expiry-validation   # para correções não-triviais
git checkout main                           # para correções triviais, direto no main
```

---

## 4. Mapeamento para o Fluxo SDD-SAAS

| Evento no fluxo SDD-SAAS | Ação git correspondente |
|---|---|
| SPEC aprovado pelo humano | `git checkout -b spec/<slug>` |
| SPRINT N recebe veredicto APROVADO | `git commit` com trailers (ver ARCHITECTURE.md seção 20) |
| SPRINT N recebe REPROVADO | Não commitar — corrija e re-execute `/review-arch` |
| Checklist Final da SPEC completo | `git merge --no-ff spec/<slug>` para main |
| `/quick-fix` aprovado | `git commit` direto em main ou branch `fix/` |
| `/pause-session` executado | Estado capturado em HANDOFF.md — nenhuma ação git obrigatória |
| Crash sem `/pause-session` | Consulte "Recuperação de Crash de Sessão" em AGENTS.md |

---

## 5. Equipes — Múltiplos Desenvolvedores

Quando múltiplos desenvolvedores trabalham no mesmo projeto:

- Cada desenvolvedor cria seu próprio branch `spec/<slug>` para a SPEC que está trabalhando
- SPECs independentes podem progredir em paralelo sem conflito (branches isolados)
- A revisão do Agente Review acontece por SPRINT dentro do branch — o merge para main é o gate de integração
- Use PRs/MRs padrão do repositório para o merge final de `spec/<slug>` → `main`
