import { TenantContext } from '../domain/tenant-context';

/**
 * Classe base para use cases que requerem contexto de tenant.
 * Injeta tenantId automaticamente do TenantContext — não é necessário passar como parâmetro.
 */
export abstract class TenantAwareUseCase<TInput, TOutput> {
  protected get tenantId(): string {
    return TenantContext.getTenantId();
  }

  abstract execute(input: TInput): Promise<TOutput>;
}

/**
 * Variante para use cases sem input (ex: listagem simples por tenant).
 */
export abstract class TenantAwareQueryUseCase<TOutput> {
  protected get tenantId(): string {
    return TenantContext.getTenantId();
  }

  abstract execute(): Promise<TOutput>;
}
