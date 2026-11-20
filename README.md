# Welcome to the Pyproject Template repository

This is a modern template for Python projects. It can be used as a starting point for building production-ready applications featuring **FastAPI**, **Streamlit**, full observability via **OpenTelemetry** and **OpenObserve**, and container/Kubernetes deployments with **Podman** and **Helm**.

This template is based on the ultra-fast Python package and dependency manager [uv](https://docs.astral.sh/uv/). The central file for project configuration is `pyproject.toml`.

---

## Best practices with Git

```ini
[user]
    name = Max Mustermann
    email = abc@domain.xyz
    signingkey = xyz
[core]
    editor = vim
[commit]
    gpgsign = true
    template = /home/abc/.gitmessage
[gpg]
    format = ssh
# If you deal with multiple git accounts:
[includeIf "gitdir:~/github/privategit"]
    path = ~/github/privategit/.gitconfig
```

The file `~/.gitmessage` is used as a template for commit messages. An example following [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```bash
$ cat .gitmessage
<type>[optional scope]: <description>

# [optional body]

# [optional footer(s)]
#
# Common commit types:
# 1. fix: patches a bug in your codebase (PATCH in SemVer).
# 2. feat: introduces a new feature (MINOR in SemVer).
# 3. BREAKING CHANGE: introduces breaking API changes (MAJOR in SemVer).
# 4. chore:, docs:, test:, style:, refactor:, perf:, ci:, build:
```

---

## Project Setup & Development

### Prerequisites

- [Python >= 3.12, < 3.15](https://www.python.org/)
- [uv (Python Packaging and Virtual Environments)](https://docs.astral.sh/uv/)
- [Pre-Commit (Managing Git hooks)](https://pre-commit.com/)
- Optional: [Podman](https://podman.io/) / [Podman Compose](https://github.com/containers/podman-compose)
- Optional: [Helm](https://helm.sh/) & [Minikube](https://minikube.sigs.k8s.io/) / Kubernetes

### Getting Started

Install all dependencies (including `dev` and `docs` dependency groups) and set up the virtual environment:

```bash
uv sync
```

To activate the virtual environment:

```bash
source .venv/bin/activate
```

To deactivate:

```bash
deactivate
```

---

## Developer Workflow & Tasks (`poe`)

This template includes [Poe the Poet](https://poethepoet.natn.io/) to streamline common development tasks:

| Command | Action |
| --- | --- |
| `uv run poe check` | Runs linting (`ruff`), format checking, and tests in one command |
| `uv run poe test` | Runs the test suite with `pytest` |
| `uv run poe test-cov` | Runs tests with terminal and HTML coverage reports (`htmlcov/`) |
| `uv run poe lint` | Checks and auto-fixes lint issues with `ruff` |
| `uv run poe format` | Formats code with `ruff format` |
| `uv run poe type-check` | Runs static type checks |
| `uv run poe dashboard` | Starts the Streamlit dashboard |
| `uv run poe docs-serve` | Serves the documentation locally with live reloading |
| `uv run poe docs-build` | Builds the static MkDocs documentation site |
| `uv run poe clean` | Cleans build caches, temp files, and artifacts |

---

## Running Applications Locally

### 1. FastAPI REST API

The FastAPI application is located in `src/pyproject_template/api/main.py`.

Run in development mode (with hot reloading):

```bash
uv run fastapi dev src/pyproject_template/api/main.py
```

Run in production mode:

```bash
uv run fastapi run src/pyproject_template/api/main.py --port 8000
```

- **Interactive API Docs (Swagger UI)**: Visit [http://localhost:8000/docs](http://localhost:8000/docs)
- **Alternative API Docs (ReDoc)**: Visit [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 2. Streamlit Dashboard

Start the Streamlit interactive dashboard:

```bash
uv run poe dashboard
# or: uv run streamlit run src/pyproject_template/dashboard/main.py
```

Access the dashboard at [http://localhost:8501](http://localhost:8501).

---

## Code Quality & Documentation

### Pre-commit Hooks

Install the pre-commit Git hooks:

```bash
pre-commit install
```

Run hooks against all files manually:

```bash
pre-commit run --all-files
```

### Linting & Formatting

We use [Ruff](https://github.com/astral-sh/ruff) for fast linting and formatting. Rules and configuration are defined in `pyproject.toml` under `[tool.ruff]`.

```bash
uv run ruff check src/ --fix
uv run ruff format src/
```

### Documentation (`mkdocs`)

Documentation is built with [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) and [mkdocs-jupyter](https://github.com/danielfrg/mkdocs-jupyter).

```bash
# Serve docs locally with live reload
uv run poe docs-serve

# Build static documentation files (output to site/)
uv run poe docs-build
```

---

## Container Deployment (Podman)

The provided multi-stage `Dockerfile` uses Red Hat UBI 9 as the base image and builds optimized runtime images (`python-dev` and `python-prd`).

### Build and Run Standalone Container

Build the container image:

```bash
podman build -t fastapi:latest . --target python-dev --no-cache
```

Run the container:

```bash
podman run -p 8000:8000 fastapi:latest
```

---

## Full Observability Stack (Podman Compose)

The repository provides a complete local telemetry stack composed of:
- **`python-app`**: FastAPI application with OpenTelemetry auto-instrumentation
- **`collector`**: OpenTelemetry Collector Contrib (`0.165.0`)
- **`openobserve`**: OpenObserve Standalone (`v1.1.2`) for logs, metrics, and traces

### Start the Stack

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml up -d
```

> [!NOTE]
> **SELinux Support**: Host volume bind-mounts in the compose files include the `:Z` flag (e.g. `./src:/app/src:Z`). This ensures rootless Podman automatically applies the appropriate SELinux security context on enforcing systems (such as Fedora, RHEL, and CentOS).

### Stop the Stack

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml down
```

To remove all persistent data volumes (resets OpenObserve database):

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml down -v
```

### Endpoints
- **FastAPI API**: [http://localhost:8000](http://localhost:8000) (Docs: [/docs](http://localhost:8000/docs))
- **OpenObserve UI**: [http://localhost:5080](http://localhost:5080)
  - Default User: `root@example.com`
  - Default Password: `Complexpass#123`
- **OTEL Collector OTLP Receiver**: `http://localhost:4318`

---

## Kubernetes Deployment (Helm)

A reproducible, production-ready Helm chart is located in [`deploy/helm/pyproject-template`](deploy/helm/pyproject-template). It deploys the FastAPI application alongside official upstream sub-charts for the **OpenTelemetry Collector** and **OpenObserve Standalone**.

### 1. Build Sub-chart Dependencies

Before deploying, fetch and verify the dependent sub-charts:

```bash
helm dependency build deploy/helm/pyproject-template
```

This downloads:
- `opentelemetry-collector` (official chart from `open-telemetry.github.io/opentelemetry-helm-charts`)
- `openobserve-standalone` (official chart from `charts.openobserve.ai`)

### 2. Deploy to Kubernetes / Minikube

```bash
# If using Minikube with a local container image:
podman save localhost/fastapi:latest | minikube image load -

# Install the Helm release
helm install pyproject deploy/helm/pyproject-template \
  --create-namespace \
  --namespace pyproject-dev
```

### 3. Check Status

```bash
kubectl get pods,svc,pvc -n pyproject-dev
```

### 4. Access Services via Port Forwarding

```bash
# Access FastAPI
kubectl port-forward -n pyproject-dev svc/pyproject-pyproject-template 8000:8000

# Access OpenObserve Dashboard
kubectl port-forward -n pyproject-dev svc/pyproject-openobserve-standalone 5080:5080
```

### 5. Uninstall

```bash
helm uninstall pyproject --namespace pyproject-dev
kubectl delete namespace pyproject-dev
```

---

## Branching Strategy

We follow [trunk-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development).

The default branch is `main`. This branch serves as the single source of truth for all environments: development (dev), acceptance (acc), and production (prd).

- **Development Environment**: Changes are deployed to the development environment by directly pushing to or merging into the `main` branch.
- **Acceptance Environment**: Deployment to the acceptance environment is triggered by creating a pre-release (release candidate).
- **Production Environment**: Deployment to the production environment is initiated by creating an official release.
