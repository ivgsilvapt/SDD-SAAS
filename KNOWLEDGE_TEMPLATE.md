# KNOWLEDGE.md — Registro de Lições Aprendidas

> **Este arquivo é append-only — nunca delete entradas, apenas adicione novas.**
> A IA lê este arquivo antes de cada sessão para evitar repetir erros já resolvidos.
> Atualize sempre que uma sessão revelar algo não-óbvio sobre o codebase, uma biblioteca ou uma regra de negócio.

---

## Seção 1 — Discoveries

Descobertas empíricas sobre o comportamento do sistema — coisas que não estão na documentação ou que contrariaram a expectativa inicial.

| Data | Área / Serviço | Descoberta | Lição |
|---|---|---|---|
| _exemplo_ | Stripe Webhooks | Validação de assinatura falha se body parser processar o body antes | Middleware de validação deve receber o raw body — configure antes do body-parser global |
| _exemplo_ | Prisma v5 | Erros dentro de `$transaction` callback não propagam o tipo correto em TypeScript | Envolva com try/catch e re-throw como AppError explicitamente |

---

## Seção 2 — Patterns That Worked

Padrões de implementação que funcionaram bem neste projeto — aceleram o trabalho e devem ser replicados.

| Data | Contexto | Padrão Usado | Por que funcionou |
|---|---|---|---|
| _exemplo_ | Testes de Use Cases | InMemoryRepository com method chaining no builder | Reduziu boilerplate de setup em ~40%; mantém testes legíveis |
| _exemplo_ | Domain Events | Coletar eventos na entidade + dispatcher no Use Case | Evita acoplamento entre camadas; domínio permanece puro |

---

## Seção 3 — Patterns to Avoid

Anti-padrões que foram tentados e falharam — nunca repita.

| Data | Anti-Padrão Tentado | Por que Falhou | Abordagem Correta |
|---|---|---|---|
| _exemplo_ | Passar tenantId como parâmetro do método | Espalhou o parâmetro por toda a cadeia de chamadas; esquecido em métodos internos | Injetar TenantContext via DI no repositório — disponível sem propagação manual |
| _exemplo_ | Mock de repositório via jest.fn() em testes de Use Case | Mock não exercita contrato real da interface; bug de integração passou despercebido | Usar InMemoryRepository que implementa a mesma interface do repositório real |

---

## Seção 4 — External API Gotchas

Comportamentos não-óbvios de SDKs e serviços externos usados neste projeto.

| Serviço | Versão | Gotcha | Workaround |
|---|---|---|---|
| _exemplo_ | Stripe SDK v12 | `paymentIntent.confirm()` lança exceção para erros de cartão (não retorna erro) | Envolva em try/catch e mapeie `StripeCardError` para `AppError` no adapter |
| _exemplo_ | SendGrid v7 | Rate limit silencioso: aceita 202 mas não envia se ultrapassar cota diária | Verifique `x-message-id` no response header para confirmar enfileiramento |
