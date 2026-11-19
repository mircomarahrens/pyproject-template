# pyproject-template Helm Chart

This Helm chart packages the FastAPI application alongside the official **OpenTelemetry Collector** and **OpenObserve Standalone** sub-charts.

## Architecture

- **FastAPI Application**: Container deployment exposing HTTP on port 8000 with liveness and readiness probes and OTLP telemetry exporter environment variables.
- **OpenTelemetry Collector Sub-chart**: Official `open-telemetry/opentelemetry-collector` chart receiving OTLP signals (gRPC `4317` and HTTP `4318`) and forwarding logs, traces, and metrics to OpenObserve.
- **OpenObserve Standalone Sub-chart**: Official `openobserve/openobserve-standalone` single-node chart providing search, storage, dashboards, and stream management on port 5080.

## Prerequisites

- Kubernetes 1.24+
- Helm 3.8+ / 4.x

## Build Dependencies

Fetch and lock the sub-charts:

```bash
helm dependency build deploy/helm/pyproject-template
```

This generates `Chart.lock` and downloads the packaged archives into `charts/`:
- `opentelemetry-collector-0.180.0.tgz`
- `openobserve-standalone-1.1.6.tgz`

## Dry-run / Template Rendering

Verify template generation without deploying to a cluster:

```bash
helm template my-release deploy/helm/pyproject-template
```

## Linting

```bash
helm lint deploy/helm/pyproject-template
```

## Installing the Chart

```bash
helm install my-stack deploy/helm/pyproject-template \
  --namespace my-namespace \
  --create-namespace \
  --values deploy/helm/pyproject-template/values.yaml
```

## Upgrading

```bash
helm upgrade my-stack deploy/helm/pyproject-template \
  --namespace my-namespace \
  --values deploy/helm/pyproject-template/values.yaml
```

## Uninstalling

```bash
helm uninstall my-stack --namespace my-namespace
```
