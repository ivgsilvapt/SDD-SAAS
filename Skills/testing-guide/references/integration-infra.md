# Integration Tests — Infraestrutura e Presentation

> Excerto temático de `TESTING_GUIDE.md` (fonte completa) — seções 2.3, 2.4, 7.

## Integration Tests — Infrastructure

**O que testar:** repositórios concretos contra banco de dados de teste real, mapeamento ORM, queries com filtros/ordenação/paginação, que o `tenantId` está sendo filtrado corretamente, migrations executadas corretamente (schema antes e depois).

**Setup:** banco de dados de teste isolado (container Docker ou em memória, ex: SQLite); limpe entre testes (transaction rollback ou truncate); nunca use o banco de desenvolvimento.

```
tests/integration/infrastructure/
├── repositories/{subscription-repository,invoice-repository}.test.ts
└── migrations/20250115_create_subscriptions.test.ts
```

## Integration Tests — Presentation

**O que testar:** status HTTP correto por cenário, corpo da resposta (campos esperados, formato do envelope), autenticação (401 sem token, 403 sem permissão), validação de input (400/422), que o controller chama o use case correto.

**Setup:** test client HTTP (sem subir servidor real); mocke o Use Case (não o repositório) — está testando a apresentação, não o domínio; use tokens JWT de teste com tenantId/userId fixos.

```
tests/integration/presentation/
├── subscriptions.controller.test.ts
└── invoices.controller.test.ts
```

## Testes de Migrations

Para cada migration que altera tabelas existentes:

```
1. Verifica estado do schema ANTES da migration
2. Executa a migration
3. Verifica estado do schema APÓS a migration
4. (Opcional) Verifica que dados existentes foram preservados/migrados corretamente
```

Migrations de criação: basta verificar que a tabela existe com as colunas corretas. Migrations de alteração: verificar o comportamento dos dados existentes após a alteração.
