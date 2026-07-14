from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    otel_service_name: str | None = None
    otel_service_instance_id: str = "default"
    otel_exporter_otlp_logs_endpoint: str | None = None
    otel_exporter_otlp_traces_endpoint: str | None = None
    otel_exporter_otlp_metrics_endpoint: str | None = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
