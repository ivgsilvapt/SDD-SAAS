export class TenantId {
  private constructor(private readonly value: string) {}

  static create(value: string): TenantId {
    if (!value || value.trim().length === 0) {
      throw new Error('TenantId cannot be empty');
    }
    if (value.length > 128) {
      throw new Error('TenantId cannot exceed 128 characters');
    }
    return new TenantId(value.trim());
  }

  static fromString(value: string): TenantId {
    return TenantId.create(value);
  }

  toString(): string {
    return this.value;
  }

  equals(other: TenantId): boolean {
    return this.value === other.value;
  }

  toJSON(): string {
    return this.value;
  }
}
