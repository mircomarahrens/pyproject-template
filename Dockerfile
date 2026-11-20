FROM registry.access.redhat.com/ubi9/python-312 AS base
#FROM ubi9/python-312 AS base

FROM ghcr.io/astral-sh/uv:0.13.9 AS uv
#FROM astral/uv:0.13.9 AS uv

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
ENV UV_PROJECT_ENVIRONMENT=/opt/app-root

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

CMD ["uv", "run", "fastapi", "run", "src/pyproject_template/api/main.py", "--host", "0.0.0.0", "--port", "8000", "--reload"]

FROM python-runtime AS python-prd

COPY --chown=1001:0 src /app/src

CMD ["uv", "run", "fastapi", "run", "src/pyproject_template/api/main.py", "--host", "0.0.0.0", "--port", "8000"]

FROM registry.access.redhat.com/ubi9/ubi:latest AS cpp-builder

RUN dnf install -y gcc-c++ cmake git make libatomic libcurl-devel && dnf clean all

WORKDIR /build
COPY cpp/roll-dice /build
RUN cmake -B out -DCMAKE_BUILD_TYPE=Release -DOATPP_BUILD_TESTS=OFF -DBUILD_TESTING=OFF && \
    cmake --build out --target dice-server -j$(nproc)

FROM registry.access.redhat.com/ubi9/ubi-minimal:latest AS cpp-prd

RUN microdnf install -y libatomic && microdnf clean all

WORKDIR /app
COPY --from=cpp-builder /build/out/dice-server /app/dice-server

USER 1001
EXPOSE 8080

CMD ["/app/dice-server"]
