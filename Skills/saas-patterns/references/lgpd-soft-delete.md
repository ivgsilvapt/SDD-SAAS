# LGPD/GDPR e Soft Delete

> Excerto temático de `SAAS_PATTERNS.md` (fonte completa) — seção 7.

## Dados Pessoais (PII)

Defina no SPEC ou no GLOSSARY quais campos são PII: nome completo, e-mail, telefone, CPF/CNPJ, IP de acesso, device ID, dados de comportamento.

## Padrões de Conformidade

| Requisito | Implementação |
|---|---|
| **Direito ao esquecimento** | Soft delete com `deletedAt`; anonimização de PII após N dias |
| **Portabilidade de dados** | Use Case `ExportTenantDataUseCase` — retorna todos os dados do tenant em JSON/CSV |
| **Consentimento** | Registre consentimento com timestamp e versão da política |
| **Retenção** | Defina TTL por tipo de dado; purge automático via job |
| **Acesso por terceiros** | API de dados só acessível pelo próprio tenant |
| **Log de acesso a PII** | Auditoria de quem acessou quais dados pessoais e quando |

## Soft Delete vs Hard Delete

```
// Soft delete — padrão para entidades com PII
Entity:
  deletedAt: Date | null
  deletedBy: UserId | null
```

**Comportamento explícito do repositório** (ver `ARCHITECTURE.md` §11):

| Método | Comportamento |
|---|---|
| `findById(id)` | Retorna `NotFoundError` se `deletedAt IS NOT NULL` |
| `findAll(filter)` | Filtra automaticamente `WHERE deletedAt IS NULL` |
| `findByIdIncludeDeleted(id)` | Retorna mesmo que deletado — apenas para auditoria/LGPD |
| `delete(id)` | Seta `deletedAt = now()` — nunca executa `DELETE` físico |

```
// Após TTL de retenção, anonimiza os dados pessoais (não deleta o registro)
AnonimizationJob:
  - Substitui nome por "Usuário removido"
  - Substitui e-mail por hash irreversível
  - Remove telefone, CPF, endereço
```

Hard delete físico é permitido apenas via `PurgePersonalDataJob`, com log de auditoria obrigatório.
