from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource

from pyproject_template.api.config import settings


def initialize_metrics(resource: Resource = None) -> MeterProvider:
    """
    Initialize OpenTelemetry metrics with OTLP exporter.
    This function sets up the meter provider and configures the metric reader.
    """
    metrics_endpoint = settings.otel_exporter_otlp_metrics_endpoint
    exporter = OTLPMetricExporter(endpoint=metrics_endpoint)
    reader = PeriodicExportingMetricReader(exporter)
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    metrics.set_meter_provider(provider)
    return provider
