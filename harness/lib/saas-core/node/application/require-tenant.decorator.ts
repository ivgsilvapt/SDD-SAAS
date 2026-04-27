import { TenantContext } from '../domain/tenant-context';

/**
 * Decorator de método que garante que TenantContext está populado antes de executar.
 * Lança UnauthorizedError se chamado fora de um contexto de tenant.
 *
 * Uso:
 *   class MyUseCase {
 *     @RequireTenant()
 *     async execute(input: Input): Promise<Output> { ... }
 *   }
 */
export function RequireTenant() {
  return function (
    _target: object,
    _propertyKey: string,
    descriptor: PropertyDescriptor,
  ): PropertyDescriptor {
    const originalMethod = descriptor.value as (...args: unknown[]) => unknown;

    descriptor.value = function (...args: unknown[]) {
      const ctx = TenantContext.currentOrNull();
      if (!ctx) {
        throw new Error(
          'RequireTenant: operation requires an authenticated tenant context. ' +
          'Ensure the request passed through tenant middleware.',
        );
      }
      return originalMethod.apply(this, args);
    };

    return descriptor;
  };
}
