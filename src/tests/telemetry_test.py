import importlib
import runpy

import pyproject_template.api.logger as logger_module
import pyproject_template.api.meter as meter_module
import pyproject_template.api.tracer as tracer_module


class _DummyProvider:
    def __init__(self, resource=None):
        self.resource = resource
        self.processors = []

    def add_log_record_processor(self, processor):
        self.processors.append(processor)


class _DummyTracerProvider:
    def __init__(self, resource=None):
        self.resource = resource
        self.processors = []

    def add_span_processor(self, processor):
        self.processors.append(processor)


class _DummyLogger:
    def __init__(self):
        self.handlers = []

    def addHandler(self, handler):
        self.handlers.append(handler)


class _DummyLoggingModule:
    INFO = 20

    def __init__(self):
        self._logger = _DummyLogger()

    def getLogger(self):
        return self._logger


def test_initialize_logging(monkeypatch):
    calls = {"set_provider": None, "endpoint": None}
    dummy_logging = _DummyLoggingModule()

    def _set_provider(provider):
        calls["set_provider"] = provider

    def _exporter(endpoint=None):
        calls["endpoint"] = endpoint
        return {"endpoint": endpoint}

    import pyproject_template.api.config as config_module

    monkeypatch.setattr(
        config_module.settings,
        "otel_exporter_otlp_logs_endpoint",
        "http://localhost:4318/v1/logs",
    )
    monkeypatch.setattr(logger_module, "LoggerProvider", _DummyProvider)
    monkeypatch.setattr(logger_module, "set_logger_provider", _set_provider)
    monkeypatch.setattr(logger_module, "OTLPLogExporter", _exporter)
    monkeypatch.setattr(
        logger_module,
        "BatchLogRecordProcessor",
        lambda exporter: {"processor": exporter},
    )
    monkeypatch.setattr(
        logger_module,
        "LoggingHandler",
        lambda level, logger_provider: {"level": level, "provider": logger_provider},
    )
    monkeypatch.setattr(logger_module, "logging", dummy_logging)

    provider = logger_module.initialize_logging(resource=None)

    assert isinstance(provider, _DummyProvider)
    assert calls["set_provider"] is provider
    assert calls["endpoint"] == "http://localhost:4318/v1/logs"
    assert len(provider.processors) == 1


def test_initialize_tracing(monkeypatch):
    calls = {"set_provider": None, "endpoint": None}

    class _TraceShim:
        def __init__(self):
            self.provider = None

        def set_tracer_provider(self, provider):
            calls["set_provider"] = provider
            self.provider = provider

        def get_tracer_provider(self):
            return self.provider

    trace_shim = _TraceShim()

    import pyproject_template.api.config as config_module

    monkeypatch.setattr(
        config_module.settings,
        "otel_exporter_otlp_traces_endpoint",
        "http://localhost:4318/v1/traces",
    )
    monkeypatch.setattr(tracer_module, "TracerProvider", _DummyTracerProvider)
    monkeypatch.setattr(
        tracer_module, "OTLPSpanExporter", lambda endpoint=None: {"endpoint": endpoint}
    )
    monkeypatch.setattr(
        tracer_module, "BatchSpanProcessor", lambda exporter: {"processor": exporter}
    )
    monkeypatch.setattr(tracer_module, "trace", trace_shim)

    provider = tracer_module.initialize_tracing(resource=None)

    assert isinstance(provider, _DummyTracerProvider)
    assert calls["set_provider"] is provider
    assert provider.processors == [
        {"processor": {"endpoint": "http://localhost:4318/v1/traces"}}
    ]


class _DummyMeterProvider:
    def __init__(self, resource=None, metric_readers=None):
        self.resource = resource
        self.metric_readers = metric_readers


def test_initialize_metrics(monkeypatch):
    calls = {"set_provider": None, "endpoint": None}

    class _MetricsShim:
        def __init__(self):
            self.provider = None

        def set_meter_provider(self, provider):
            calls["set_provider"] = provider
            self.provider = provider

        def get_meter_provider(self):
            return self.provider

    metrics_shim = _MetricsShim()

    import pyproject_template.api.config as config_module

    monkeypatch.setattr(
        config_module.settings,
        "otel_exporter_otlp_metrics_endpoint",
        "http://localhost:4318/v1/metrics",
    )
    monkeypatch.setattr(meter_module, "MeterProvider", _DummyMeterProvider)
    monkeypatch.setattr(
        meter_module, "OTLPMetricExporter", lambda endpoint=None: {"endpoint": endpoint}
    )
    monkeypatch.setattr(
        meter_module,
        "PeriodicExportingMetricReader",
        lambda exporter: {"reader": exporter},
    )
    monkeypatch.setattr(meter_module, "metrics", metrics_shim)

    provider = meter_module.initialize_metrics(resource=None)

    assert isinstance(provider, _DummyMeterProvider)
    assert calls["set_provider"] is provider
    assert provider.metric_readers == [
        {"reader": {"endpoint": "http://localhost:4318/v1/metrics"}}
    ]


def test_otel_module_initialization(monkeypatch):
    calls = {"log": None, "trace": None, "metrics": None, "instrumented": False}

    def _init_log(resource):
        calls["log"] = resource

    def _init_trace(resource):
        calls["trace"] = resource
        return "trace-provider"

    def _init_metrics(resource):
        calls["metrics"] = resource
        return "metrics-provider"

    class _DummyInstrumentor:
        @staticmethod
        def instrument_app(app, tracer_provider=None, meter_provider=None):
            calls["instrumented"] = True
            calls["tracer_provider"] = tracer_provider
            calls["meter_provider"] = meter_provider

    import pyproject_template.api.config as config_module

    monkeypatch.setattr(config_module.settings, "otel_service_name", "fastapi-app")
    monkeypatch.setattr(
        config_module.settings, "otel_service_instance_id", "instance-1"
    )
    monkeypatch.setattr("pyproject_template.api.logger.initialize_logging", _init_log)
    monkeypatch.setattr("pyproject_template.api.tracer.initialize_tracing", _init_trace)
    monkeypatch.setattr(
        "pyproject_template.api.meter.initialize_metrics", _init_metrics
    )
    monkeypatch.setattr(
        "opentelemetry.instrumentation.fastapi.FastAPIInstrumentor", _DummyInstrumentor
    )

    class DummyApp:
        class State:
            pass

        def __init__(self):
            self.state = DummyApp.State()

    dummy_app = DummyApp()
    otel_module = importlib.import_module("pyproject_template.api.otel")
    importlib.reload(otel_module)
    otel_module.setup_telemetry(dummy_app)

    assert calls["log"] is not None
    assert calls["trace"] is not None
    assert calls["metrics"] is not None
    assert calls["instrumented"] is True
    assert calls["tracer_provider"] == "trace-provider"
    assert calls["meter_provider"] == "metrics-provider"
    assert dummy_app.state.trace_provider == "trace-provider"
    assert dummy_app.state.meter_provider == "metrics-provider"


def test_main_module_runs_as_script(capsys):
    runpy.run_module("pyproject_template.main", run_name="__main__")
    captured = capsys.readouterr()
    assert "Result: 21" in captured.out
