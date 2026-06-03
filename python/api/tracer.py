import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor


def initialize_tracing(resource: Resource = None) -> TracerProvider:
    """
    Initialize OpenTelemetry tracing with a console exporter.
    This function sets up the tracer provider and configures the span processor.
    """

    # Set up tracer provider and span processor
    provider = TracerProvider(resource=resource)

    # Sets the global default tracer provider
    trace.set_tracer_provider(provider)

    # Set up OTLP exporter for spans
    trace_endpoint = os.getenv("OTEL_EXPORTER_OTLP_TRACES_ENDPOINT")
    otlp_exporter = OTLPSpanExporter(endpoint=trace_endpoint)
    processor = BatchSpanProcessor(otlp_exporter)
    trace.get_tracer_provider().add_span_processor(processor)

    return provider
