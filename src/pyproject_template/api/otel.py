import os

from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.resources import Resource

from pyproject_template.api.logger import initialize_logging
from pyproject_template.api.main import app
from pyproject_template.api.tracer import initialize_tracing

# Setup resource (optional: add more attributes)
resource = Resource(
    attributes={
        "service.name": os.getenv("OTEL_SERVICE_NAME"),
        "service.instance.id": os.getenv("OTEL_SERVICE_INSTANCE_ID"),
    }
)

# Initialize OpenTelemetry logging
initialize_logging(resource=resource)

# Initialize OpenTelemetry tracing
trace_provider = initialize_tracing(resource=resource)

# Initialize OpenTelemetry metrics (if needed)
meter_provider = None  # Placeholder for future metrics initialization

# Instrument FastAPI with OpenTelemetry
FastAPIInstrumentor.instrument_app(
    app, tracer_provider=trace_provider, meter_provider=meter_provider
)
