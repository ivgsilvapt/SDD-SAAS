# STATE.md — Memória Persistente do Projeto

> **Como usar:** Copie este arquivo para `STATE.md` na raiz do seu projeto SaaS.
> O CLAUDE.md já o carrega automaticamente em toda sessão (`@STATE.md`).
> Atualize após qualquer sessão em que uma decisão não-óbvia foi tomada.
> **Limite operacional:** mantenha o STATE.md ativo com até ~150 linhas. O `/retrospect` verifica esse limite e propõe mover decisões encerradas e sessões antigas para `STATE_ARCHIVE.md` (mesma estrutura de seções deste arquivo). Arquivar não é apagar — apenas mova o conteúdo para preservar a memória de longo prazo sem pagar o custo de tokens em toda sessão.

---

## 1. Decisões Arquiteturais

Registre aqui decisões tomadas que a IA precisa conhecer em sessões futuras.
Cada decisão evita que a IA re-proponha alternativas já descartadas.

| Data | Decisão | Alternativas Consideradas | Raciocínio | Impacto |
|---|---|---|---|---|
| AAAA-MM-DD | *ex: Row-Level Isolation para multi-tenancy* | *ex: Schema-per-tenant, Database-per-tenant* | *ex: Simplicidade operacional no volume atual; migrations únicas para todos os tenants* | *ex: Toda entidade de domínio tem campo `tenant_id`; toda query filtra por `TenantContext`* |
| AAAA-MM-DD | | | | |

---

## 2. Bloqueios Ativos

Registre impedimentos em aberto. Remova a linha (com nota "Resolvido em AAAA-MM-DD") quando o bloqueio for superado.

| Aberto em | Descrição | Bloqueia | Responsável | Status |
|---|---|---|---|---|
| AAAA-MM-DD | *ex: Dependência da API de pagamento sem documentação de sandbox* | *ex: SPRINT 3 do SPEC billing/create-subscription* | *ex: Time de integrações* | *em aberto* |

---

## 3. Ideias Adiadas (Parking Lot)

Ideias boas que chegaram antes da hora. Registrar evita gold-plating no SPRINT errado e garante que a ideia não se perca.

| Data | Ideia | Por que adiada | Gatilho para revisitar |
|---|---|---|---|
| AAAA-MM-DD | *ex: Cache de planos por tenant em Redis* | *ex: YAGNI — temos < 100 tenants em beta; latência atual é aceitável* | *ex: Quando ultrapassar 500 tenants ativos ou latência de /plans > 200ms* |

---

## 4. Log de Sessões

Registro cronológico reverso das sessões. O `/pause-session` atualiza esta seção automaticamente.

| Data | O que foi feito | O que ficou em aberto | SPRINT/SPEC referência |
|---|---|---|---|
| AAAA-MM-DD | *ex: SPRINT 1 do billing/create-subscription implementado e aprovado pelo Review* | *ex: Nenhum — SPRINT 2 é o próximo passo* | *billing/create-subscription SPRINT 1* |
| AAAA-MM-DD | *ex: SPEC de billing/cancel-subscription criado e aprovado. Aguarda Analyze.* | *ex: Clarify: o que acontece com dias restantes ao cancelar? Definido: sem estorno, acesso até fim do período* | *billing/cancel-subscription* |
