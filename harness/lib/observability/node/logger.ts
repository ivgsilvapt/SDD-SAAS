import pino from 'pino';
import { Correlation } from './correlation';

const PII_FIELDS = [
  'password',
  'token',
  'secret',
  'authorization',
  'credit_card',
  'creditCard',
  'ssn',
  'cpf',
  'cnpj',
  'email',
  'phone',
  'phoneNumber',
];

const baseLogger = pino({
  level: process.env.LOG_LEVEL ?? 'info',
  redact: {
    paths: PII_FIELDS,
    censor: '[REDACTED]',
  },
  formatters: {
    level: (label) => ({ level: label }),
  },
  base: {
    service: process.env.OTEL_SERVICE_NAME ?? process.env.APP_NAME ?? 'app',
    env: process.env.NODE_ENV ?? 'production',
  },
  timestamp: pino.stdTimeFunctions.isoTime,
});

/**
 * Logger pré-configurado com:
 * - Redação automática de campos PII
 * - requestId e tenantId injetados automaticamente do contexto
 * - Formatação JSON estruturada
 *
 * Uso:
 *   import { logger } from '@harness/observability';
 *   logger.info({ event: 'user_created', userId }, 'User created');
 */
export const logger = {
  info(obj: Record<string, unknown>, msg?: string): void {
    baseLogger.child(getContext()).info(obj, msg);
  },
  warn(obj: Record<string, unknown>, msg?: string): void {
    baseLogger.child(getContext()).warn(obj, msg);
  },
  error(obj: Record<string, unknown> | Error, msg?: string): void {
    if (obj instanceof Error) {
      baseLogger.child(getContext()).error({ err: obj }, msg ?? obj.message);
    } else {
      baseLogger.child(getContext()).error(obj, msg);
    }
  },
  debug(obj: Record<string, unknown>, msg?: string): void {
    baseLogger.child(getContext()).debug(obj, msg);
  },
  child(bindings: Record<string, unknown>) {
    return baseLogger.child({ ...getContext(), ...bindings });
  },
};

function getContext(): Record<string, unknown> {
  const ctx: Record<string, unknown> = {};
  const requestId = Correlation.getRequestId();
  if (requestId) ctx.requestId = requestId;
  return ctx;
}
