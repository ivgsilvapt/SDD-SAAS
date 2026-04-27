import { AsyncLocalStorage } from 'async_hooks';

interface TenantContextData {
  tenantId: string;
  userId?: string;
}

const storage = new AsyncLocalStorage<TenantContextData>();

export const TenantContext = {
  /**
   * Executa fn com o tenantId definido no contexto.
   * Uso: await TenantContext.run('tenant-123', () => someUseCase.execute(...))
   */
  run<T>(tenantId: string, fn: () => T | Promise<T>, userId?: string): Promise<T> {
    return new Promise<T>((resolve, reject) => {
      storage.run({ tenantId, userId }, () => {
        Promise.resolve(fn()).then(resolve, reject);
      });
    });
  },

  /**
   * Retorna o contexto atual. Lança se chamado fora de um TenantContext.run().
   */
  current(): TenantContextData {
    const ctx = storage.getStore();
    if (!ctx) {
      throw new Error(
        'TenantContext.current() called outside of a tenant context. ' +
        'Ensure your request handler sets up TenantContext via tenant middleware.',
      );
    }
    return ctx;
  },

  currentOrNull(): TenantContextData | null {
    return storage.getStore() ?? null;
  },

  getTenantId(): string {
    return TenantContext.current().tenantId;
  },

  tryGetTenantId(): string | null {
    return storage.getStore()?.tenantId ?? null;
  },
};
