import { AsyncLocalStorage } from 'async_hooks';
import { randomUUID } from 'crypto';

interface CorrelationData {
  requestId: string;
}

const storage = new AsyncLocalStorage<CorrelationData>();

export const Correlation = {
  run<T>(fn: () => T | Promise<T>, requestId?: string): Promise<T> {
    const id = requestId ?? randomUUID();
    return new Promise<T>((resolve, reject) => {
      storage.run({ requestId: id }, () => {
        Promise.resolve(fn()).then(resolve, reject);
      });
    });
  },

  getRequestId(): string | undefined {
    return storage.getStore()?.requestId;
  },

  requireRequestId(): string {
    const id = storage.getStore()?.requestId;
    if (!id) throw new Error('No requestId in current context');
    return id;
  },
};

/**
 * Express/NestJS middleware que injeta requestId em cada request.
 * Lê X-Request-ID do header se presente, caso contrário gera um novo UUID.
 */
export function correlationMiddleware(
  req: { headers: Record<string, string | string[] | undefined> },
  res: { setHeader(name: string, value: string): void },
  next: () => void,
): void {
  const existing = req.headers['x-request-id'];
  const requestId = (Array.isArray(existing) ? existing[0] : existing) ?? randomUUID();
  res.setHeader('X-Request-ID', requestId);
  Correlation.run(() => next(), requestId).catch(() => next());
}
