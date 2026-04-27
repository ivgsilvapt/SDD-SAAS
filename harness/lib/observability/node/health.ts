interface HealthCheck {
  name: string;
  check(): Promise<void>;
}

interface HealthStatus {
  status: 'ok' | 'degraded' | 'down';
  checks: Record<string, { status: 'ok' | 'error'; error?: string }>;
  timestamp: string;
}

const checks: HealthCheck[] = [];

export function registerHealthCheck(check: HealthCheck): void {
  checks.push(check);
}

async function runHealthChecks(): Promise<HealthStatus> {
  const results: HealthStatus['checks'] = {};
  let overallStatus: HealthStatus['status'] = 'ok';

  await Promise.allSettled(
    checks.map(async (check) => {
      try {
        await check.check();
        results[check.name] = { status: 'ok' };
      } catch (err) {
        results[check.name] = {
          status: 'error',
          error: err instanceof Error ? err.message : String(err),
        };
        overallStatus = 'down';
      }
    }),
  );

  return {
    status: overallStatus,
    checks: results,
    timestamp: new Date().toISOString(),
  };
}

/**
 * Cria um Express Router com endpoints /health/live e /health/ready.
 *
 * Uso:
 *   import express from 'express';
 *   import { createHealthRouter, registerHealthCheck } from '@harness/observability';
 *
 *   registerHealthCheck({
 *     name: 'database',
 *     check: async () => { await db.raw('SELECT 1') },
 *   });
 *
 *   app.use(createHealthRouter());
 */
export function createHealthRouter() {
  // Retorna um objeto compatível com Express Router sem importar Express diretamente
  const routes: Array<{ path: string; handler: (req: unknown, res: { json: (data: unknown) => void; status: (code: number) => { json: (data: unknown) => void } }) => void }> = [];

  routes.push({
    path: '/health/live',
    handler: (_req, res) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    },
  });

  routes.push({
    path: '/health/ready',
    handler: async (_req, res) => {
      const result = await runHealthChecks();
      const statusCode = result.status === 'ok' ? 200 : 503;
      res.status(statusCode).json(result);
    },
  });

  return routes;
}
