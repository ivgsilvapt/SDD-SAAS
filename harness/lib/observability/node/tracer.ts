import { NodeSDK } from '@opentelemetry/sdk-node';
import { OTLPTraceExporter } from '@opentelemetry/exporter-trace-otlp-http';
import { Resource } from '@opentelemetry/resources';
import { SEMRESATTRS_SERVICE_NAME } from '@opentelemetry/semantic-conventions';
import { getNodeAutoInstrumentations } from '@opentelemetry/auto-instrumentations-node';
import { trace } from '@opentelemetry/api';

let sdk: NodeSDK | null = null;

/**
 * Inicializa o OpenTelemetry SDK com exportador OTLP.
 * Chame uma vez no bootstrap da aplicação, antes de carregar outros módulos.
 *
 * Uso:
 *   import { initTracing } from '@harness/observability';
 *   initTracing(); // no topo do main.ts
 */
export function initTracing(serviceName?: string): void {
  const name = serviceName ?? process.env.OTEL_SERVICE_NAME ?? process.env.APP_NAME ?? 'app';
  const endpoint = process.env.OTEL_EXPORTER_OTLP_ENDPOINT ?? 'http://localhost:4318';

  sdk = new NodeSDK({
    resource: new Resource({ [SEMRESATTRS_SERVICE_NAME]: name }),
    traceExporter: new OTLPTraceExporter({ url: `${endpoint}/v1/traces` }),
    instrumentations: [getNodeAutoInstrumentations()],
  });

  sdk.start();

  process.on('SIGTERM', async () => {
    await sdk?.shutdown();
  });
}

export function getTracer(name: string) {
  return trace.getTracer(name);
}

export function withSpan<T>(
  tracerName: string,
  spanName: string,
  fn: () => T | Promise<T>,
): Promise<T> {
  const tracer = getTracer(tracerName);
  const span = tracer.startSpan(spanName);
  return Promise.resolve(fn())
    .then((result) => {
      span.end();
      return result;
    })
    .catch((err: Error) => {
      span.recordException(err);
      span.end();
      throw err;
    });
}
