import logging
import os

# Logging is in status experimental (marked by _), so it may change in future releases.
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.resources import Resource


def initialize_logging(resource: Resource = None) -> LoggerProvider:
    """
    Initialize OpenTelemetry logging with OTLP exporter.
    This function sets up the logger provider and configures the logging handler.
    """

    # Set up logger provider
    provider = LoggerProvider(resource=resource)
    set_logger_provider(provider)

    # Set up OTLP exporter (to send to OpenTelemetry Collector)
    logs_endpoint = os.getenv("OTEL_EXPORTER_OTLP_LOGS_ENDPOINT")
    otlp_exporter = OTLPLogExporter(endpoint=logs_endpoint)
    provider.add_log_record_processor(BatchLogRecordProcessor(otlp_exporter))

    # Set up logging handler
    otel_handler = LoggingHandler(level=logging.INFO, logger_provider=provider)
    logging.getLogger().addHandler(otel_handler)

    return provider
