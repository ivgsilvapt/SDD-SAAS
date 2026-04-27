export interface TenantProps {
  id: string;
  slug: string;
  name: string;
  status: 'active' | 'suspended' | 'cancelled' | 'trial';
  plan: 'free' | 'basic' | 'pro' | 'enterprise';
  createdAt: Date;
}

export class TenantBuilder {
  private props: TenantProps = {
    id: 'tenant-test-01',
    slug: 'test-tenant',
    name: 'Test Tenant',
    status: 'active',
    plan: 'pro',
    createdAt: new Date('2025-01-01T00:00:00Z'),
  };

  withId(id: string): this {
    this.props.id = id;
    return this;
  }

  withSlug(slug: string): this {
    this.props.slug = slug;
    return this;
  }

  withName(name: string): this {
    this.props.name = name;
    return this;
  }

  withStatus(status: TenantProps['status']): this {
    this.props.status = status;
    return this;
  }

  withPlan(plan: TenantProps['plan']): this {
    this.props.plan = plan;
    return this;
  }

  withCreatedAt(date: Date): this {
    this.props.createdAt = date;
    return this;
  }

  build(): TenantProps {
    return { ...this.props };
  }

  buildMany(count: number): TenantProps[] {
    return Array.from({ length: count }, (_, i) => ({
      ...this.props,
      id: `${this.props.id}-${i + 1}`,
      slug: `${this.props.slug}-${i + 1}`,
    }));
  }
}

export function aTenant(): TenantBuilder {
  return new TenantBuilder();
}
