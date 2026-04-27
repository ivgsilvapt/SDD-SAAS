export interface TenantScoped {
  id: string;
  tenantId: string;
}

export interface InMemoryRepository<T extends TenantScoped> {
  findById(id: string, tenantId: string): Promise<T | null>;
  save(item: T): Promise<void>;
  delete(id: string, tenantId: string): Promise<void>;
  findAllByTenant(tenantId: string): Promise<T[]>;
  findAll(): Promise<T[]>;
  count(tenantId?: string): Promise<number>;
  _reset(): void;
  _store(): Map<string, T>;
}

/**
 * Cria um repositório in-memory com isolamento por tenantId para uso em testes.
 * O filtro de tenantId é aplicado por padrão em todas as operações — bug clássico
 * de multi-tenant (esquecer o filtro) torna-se impossível.
 */
export function createInMemoryRepository<T extends TenantScoped>(): InMemoryRepository<T> {
  const store = new Map<string, T>();

  return {
    async findById(id: string, tenantId: string): Promise<T | null> {
      const item = store.get(id);
      if (!item) return null;
      return item.tenantId === tenantId ? item : null;
    },

    async save(item: T): Promise<void> {
      store.set(item.id, { ...item });
    },

    async delete(id: string, tenantId: string): Promise<void> {
      const item = store.get(id);
      if (item?.tenantId === tenantId) {
        store.delete(id);
      }
    },

    async findAllByTenant(tenantId: string): Promise<T[]> {
      return Array.from(store.values()).filter((item) => item.tenantId === tenantId);
    },

    async findAll(): Promise<T[]> {
      return Array.from(store.values());
    },

    async count(tenantId?: string): Promise<number> {
      if (tenantId) {
        return Array.from(store.values()).filter((i) => i.tenantId === tenantId).length;
      }
      return store.size;
    },

    _reset(): void {
      store.clear();
    },

    _store(): Map<string, T> {
      return store;
    },
  };
}
