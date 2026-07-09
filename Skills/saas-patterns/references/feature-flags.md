# Feature Flags

> Excerto temático de `SAAS_PATTERNS.md` (fonte completa) — seção 4.

Feature flags permitem rollout gradual, testes A/B e diferenciação por plano.

## Interface no Domínio

```
// domain/shared/feature-flags/IFeatureFlagService.ts
interface IFeatureFlagService {
  isEnabled(flag: FeatureFlag, tenantId: TenantId): boolean
}

enum FeatureFlag {
  ADVANCED_REPORTS   = 'advanced_reports',
  API_ACCESS         = 'api_access',
  CUSTOM_DOMAIN      = 'custom_domain',
  TEAM_MEMBERS       = 'team_members',
  EXPORT_CSV         = 'export_csv',
}
```

## Uso no Use Case

```
class ExportReportUseCase {
  constructor(
    private featureFlags: IFeatureFlagService,
    private tenantCtx: ITenantContext,
    private reportRepo: IReportRepository
  ) {}

  execute(): Result<ReportData> {
    if (!this.featureFlags.isEnabled(FeatureFlag.ADVANCED_REPORTS, this.tenantCtx.tenantId)) {
      return Result.fail(new AuthorizationError('FEATURE_NOT_AVAILABLE_ON_PLAN'))
    }
    // ...
  }
}
```

## Fontes de Feature Flags (Infrastructure)

| Fonte | Quando usar |
|---|---|
| Banco de dados (tabela `tenant_features`) | Feature flags por tenant ou por plano — padrão |
| Variável de ambiente | Feature flags globais (liga/desliga para todos) |
| Serviço externo (LaunchDarkly, Unleash) | Rollout gradual com percentual, A/B testing |
