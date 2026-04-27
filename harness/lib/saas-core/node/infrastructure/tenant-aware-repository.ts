import { TenantContext } from '../domain/tenant-context';
import { TenantAwareEntity } from '../domain/tenant-aware-entity';

/**
 * Classe base para repositórios com isolamento automático por tenant.
 * Qualquer query herdada aplica WHERE tenant_id = [current tenant] implicitamente.
 * Impossível esquecer o filtro de tenant — ele está na classe base.
 */
export abstract class TenantAwareRepository<T extends TenantAwareEntity> {
  /**
   * tenantId atual extraído do TenantContext.
   * Lança se chamado fora de um contexto de tenant.
   */
  protected get currentTenantId(): string {
    return TenantContext.getTenantId();
  }

  /**
   * Verifica se uma entidade pertence ao tenant atual antes de retorná-la.
   * Use em métodos findById para garantir isolamento.
   */
  protected assertBelongsToCurrentTenant(entity: T | null): T | null {
    if (!entity) return null;
    if (!entity.belongsTo(this.currentTenantId)) return null;
    return entity;
  }

  /**
   * Filtra uma lista de entidades para retornar apenas as do tenant atual.
   */
  protected filterByCurrentTenant(entities: T[]): T[] {
    const tenantId = this.currentTenantId;
    return entities.filter((e) => e.belongsTo(tenantId));
  }

  abstract findById(id: string): Promise<T | null>;
  abstract save(entity: T): Promise<void>;
  abstract delete(id: string): Promise<void>;
  abstract findAll(): Promise<T[]>;
}
