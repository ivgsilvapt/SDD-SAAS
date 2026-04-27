# Harness Template: Go Multi-Stage Dockerfile (scratch image)
# Placeholders: {{GO_VERSION}}, {{BINARY_NAME}}, {{PORT}}

# ── Stage 1: build ──────────────────────────────────────────────────────────
FROM golang:{{GO_VERSION}}-alpine AS builder
WORKDIR /app
RUN apk add --no-cache git ca-certificates tzdata
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 \
    go build -ldflags="-w -s" -o /{{BINARY_NAME}} ./cmd/server

# ── Stage 2: runtime (scratch — imagem mínima) ───────────────────────────────
FROM scratch AS runtime
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY --from=builder /{{BINARY_NAME}} /{{BINARY_NAME}}

EXPOSE {{PORT}}

HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD ["/{{BINARY_NAME}}", "healthcheck"]

ENTRYPOINT ["/{{BINARY_NAME}}"]
