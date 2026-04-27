import { TenantId } from './tenant-id';

export abstract class TenantAwareEntity {
  protected constructor(
    public readonly id: string,
    public readonly tenantId: string,
    public readonly createdAt: Date = new Date(),
  ) {
    if (!id) throw new Error(`${this.constructor.name}: id is required`);
    if (!tenantId) throw new Error(`${this.constructor.name}: tenantId is required`);
  }

  getTenantId(): TenantId {
    return TenantId.fromString(this.tenantId);
  }

  belongsTo(tenantId: string): boolean {
    return this.tenantId === tenantId;
  }

  toJSON(): Record<string, unknown> {
    return {
      id: this.id,
      tenantId: this.tenantId,
      createdAt: this.createdAt.toISOString(),
    };
  }
}
