import { collectDefaultMetrics as promCollectDefaultMetrics, Counter, Histogram, Registry } from 'prom-client';

export const registry = new Registry();

export const httpRequestsTotal = new Counter({
  name: 'http_requests_total',
  help: 'Total number of HTTP requests',
  labelNames: ['method', 'route', 'status_code'],
  registers: [registry],
});

export const httpRequestDurationMs = new Histogram({
  name: 'http_request_duration_ms',
  help: 'HTTP request duration in milliseconds',
  labelNames: ['method', 'route', 'status_code'],
  buckets: [5, 10, 25, 50, 100, 250, 500, 1000, 2500, 5000],
  registers: [registry],
});

export const activeRequests = new Counter({
  name: 'http_active_requests',
  help: 'Number of currently active HTTP requests',
  registers: [registry],
});

export function collectDefaultMetrics(): void {
  promCollectDefaultMetrics({ register: registry });
}

/**
 * Express middleware que registra métricas HTTP automaticamente.
 * Uso: app.use(metricsMiddleware)
 */
export function metricsMiddleware(
  req: { method: string; path?: string; route?: { path: string } },
  res: { statusCode: number; on(event: string, fn: () => void): void },
  next: () => void,
): void {
  const start = Date.now();
  activeRequests.inc();

  res.on('finish', () => {
    const route = req.route?.path ?? req.path ?? 'unknown';
    const labels = {
      method: req.method,
      route,
      status_code: String(res.statusCode),
    };
    httpRequestsTotal.inc(labels);
    httpRequestDurationMs.observe(labels, Date.now() - start);
    activeRequests.inc(-1);
  });

  next();
}
