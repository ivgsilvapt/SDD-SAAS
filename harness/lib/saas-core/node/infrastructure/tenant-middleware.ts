import { TenantContext } from '../domain/tenant-context';

interface JwtPayload {
  sub?: string;
  tenant_id?: string;
  tenantId?: string;
  [key: string]: unknown;
}

/**
 * Extrai tenantId de um JWT decodificado e popula o TenantContext.
 * Adaptadores para Express e NestJS incluídos.
 * O JWT deve conter o claim `tenant_id` (ou `tenantId`).
 */

/**
 * Decodifica o payload do JWT sem verificar assinatura.
 * Use apenas após verificação de assinatura pelo middleware de autenticação.
 */
export function decodeJwtPayload(token: string): JwtPayload {
  const parts = token.split('.');
  if (parts.length !== 3) {
    throw new Error('Invalid JWT format');
  }
  const payload = parts[1];
  const decoded = Buffer.from(payload, 'base64url').toString('utf-8');
  return JSON.parse(decoded) as JwtPayload;
}

export function extractTenantIdFromPayload(payload: JwtPayload): string {
  const tenantId = payload.tenant_id ?? payload.tenantId;
  if (!tenantId || typeof tenantId !== 'string') {
    throw new Error(
      'JWT missing tenant_id claim. Ensure the authentication token includes tenant context.',
    );
  }
  return tenantId;
}

/**
 * Express middleware.
 * Uso: app.use(tenantMiddleware)
 * Requer que req.headers.authorization contenha o Bearer token já verificado.
 */
export function tenantMiddleware(
  req: { headers: { authorization?: string }; user?: JwtPayload },
  _res: unknown,
  next: (err?: Error) => void,
): void {
  try {
    let payload: JwtPayload | null = null;

    if (req.user) {
      payload = req.user;
    } else if (req.headers.authorization) {
      const token = req.headers.authorization.replace('Bearer ', '');
      payload = decodeJwtPayload(token);
    }

    if (!payload) {
      return next(new Error('No authentication context found'));
    }

    const tenantId = extractTenantIdFromPayload(payload);
    const userId = typeof payload.sub === 'string' ? payload.sub : undefined;

    TenantContext.run(tenantId, () => next(), userId).catch(next);
  } catch (err) {
    next(err as Error);
  }
}
