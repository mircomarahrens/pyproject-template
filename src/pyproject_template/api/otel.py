from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

from pyproject_template.api.config import settings
from pyproject_template.api.logger import initialize_logging
from pyproject_template.api.meter import initialize_metrics
from pyproject_template.api.tracer import initialize_tracing


def setup_telemetry(app: FastAPI) -> None:
    """
    Initialize OpenTelemetry logging, tracing, and instrument the FastAPI app.
    Only executes if OTEL_SERVICE_NAME environment variable is set.
    """
    service_name = settings.otel_service_name
    if not service_name:
        return

    # Setup resource
    resource = Resource(
        attributes={
            "service.name": service_name,
            "service.instance.id": settings.otel_service_instance_id,
        }
    )

    # Initialize OpenTelemetry logging
    initialize_logging(resource=resource)

    # Initialize OpenTelemetry tracing
    trace_provider = initialize_tracing(resource=resource)
    app.state.trace_provider = trace_provider

    # Initialize OpenTelemetry metrics
    meter_provider = initialize_metrics(resource=resource)
    app.state.meter_provider = meter_provider

    # Instrument FastAPI with OpenTelemetry
    FastAPIInstrumentor.instrument_app(
        app, tracer_provider=trace_provider, meter_provider=meter_provider
    )
