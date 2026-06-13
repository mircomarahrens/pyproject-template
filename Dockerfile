FROM registry.access.redhat.com/ubi9/python-312 AS base
#FROM ubi9/python-312 AS base

FROM ghcr.io/astral-sh/uv:0.8.4 AS uv
#FROM astral/uv:0.8.4 AS uv

FROM base AS python-runtime
COPY --from=uv /uv /uvx /bin/

WORKDIR /app

# 1) Accept proxies as build args (coming from compose)
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NO_PROXY
ARG PIP_INDEX_URL

# 2) Export them as ENV for all subsequent RUN steps
ENV HTTP_PROXY=${HTTP_PROXY}
ENV HTTPS_PROXY=${HTTPS_PROXY}
ENV NO_PROXY=${NO_PROXY}
ENV PIP_INDEX_URL=${PIP_INDEX_URL}

# 3) Also export uv’s own proxy envs (uv honors both, but this is explicit)
ENV UV_HTTP_PROXY=${HTTPS_PROXY:-$HTTP_PROXY}
ENV UV_HTTPS_PROXY=${HTTPS_PROXY}
ENV UV_NO_PROXY=${NO_PROXY}
ENV UV_INDEX_URL=${PIP_INDEX_URL}
ENV UV_EXTRA_INDEX_URL=""

ENV GIT_PYTHON_REFRESH=quiet \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=1000

COPY --chown=1001:0 pyproject.toml uv.lock ./

USER 1001

RUN uv sync --locked

FROM python-runtime AS python-dev

RUN uv sync --locked --all-extras --dev

COPY --chown=1001:0 src /app/src

CMD ["uv", "run", "fastapi", "run", "src/pyproject_template/api/otel.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python-runtime AS python-prd

COPY --chown=1001:0 src /app/src

CMD ["uv", "run", "fastapi", "run", "src/pyproject_template/api/otel.py", "--host", "0.0.0.0", "--port", "8000"]

#FROM base AS cpp-prd
