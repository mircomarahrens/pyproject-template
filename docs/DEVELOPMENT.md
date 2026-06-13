# Development Guide

This guide covers local development setup, architecture, and common development tasks.

## Prerequisites

- **Python**: 3.10+ (see `pyproject.toml` for version constraints)
- **uv**: Package and project manager (install from [astral.sh/uv](https://docs.astral.sh/uv/))
- **Git**: For version control
- **Docker** (optional): For containerized development

## Local Setup

### Initial Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mircomarahrens/pyproject-template.git
   cd pyproject-template
   ```

2. **Install dependencies**:

   ```bash
   uv sync --dev
   ```

   This installs both runtime and development dependencies, including pre-commit hooks.

3. **Verify setup**:

   ```bash
   uv run poe test
   ```

### Using Virtual Environment

The `.venv` directory is automatically created by `uv`. Activate it with:

```bash
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

## Project Structure

```text
pyproject-template/
├── src/pyproject_template/      # Main package
│   ├── __init__.py
│   ├── arithmetic.py            # Core logic example
│   ├── main.py                  # Entry point
│   └── api/                     # FastAPI application
│       ├── main.py              # FastAPI app definition
│       ├── logger.py            # Logging setup
│       ├── tracer.py            # OpenTelemetry tracing
│       ├── meter.py             # OpenTelemetry metrics
│       └── otel.py              # OpenTelemetry integration
├── src/tests/                   # Test suite
│   ├── app_test.py              # Application tests
│   └── server_test.py           # Server/API tests
├── docs/                        # Documentation
├── examples/                    # Example notebooks and scripts
├── config/                      # Configuration files
│   └── otel/                    # OpenTelemetry config
├── cpp/                         # C++ components (optional)
└── pyproject.toml               # Project configuration
```

## Common Development Tasks

### Running Tests

```bash
# Run all tests
uv run poe test

# Run with coverage report
uv run poe test-cov

# Run only unit tests
uv run poe test-unit

# Run integration tests
uv run poe test-integration

# Run with verbose output
uv run poe test-verbose
```

### Code Quality

```bash
# Run linter (with fixes)
uv run poe lint

# Format code
uv run poe format

# Check formatting (no changes)
uv run poe format-check

# Type checking
uv run poe type-check

# Run all checks at once
uv run poe check
```

### Documentation

```bash
# Build documentation
uv run poe docs-build

# Serve documentation locally (http://localhost:8000)
uv run poe docs-serve

# Deploy documentation (requires setup)
uv run poe docs-deploy
```

### Cleanup

```bash
# Remove build artifacts, cache files, and test outputs
uv run poe clean
```

## Running the Application

### FastAPI Server (Development)

```bash
# Start development server with auto-reload
uv run fastapi run src/pyproject_template/api/main.py

# Or with OpenTelemetry instrumentation
uv run fastapi run src/pyproject_template/api/otel.py
```

Server runs on `http://localhost:8000` with interactive docs at `/docs`.

### Docker

```bash
# Build image
docker build -t fastapi:latest .

# Run development container
docker compose -f compose.python.dev.yaml up

# Run production container
docker compose -f compose.python.yaml up
```

## Writing Code

### Style Guide

- **Line length**: 88 characters (enforced by Ruff formatter)
- **Import style**: Alphabetical, with isort integration via Ruff
- **Type hints**: Required for function signatures and returns
- **Docstrings**: Google-style for public functions and classes

Example:

```python
def add_numbers(n1: int, n2: int) -> int:
    """Add two numbers.
    
    Args:
        n1: First number
        n2: Second number
    
    Returns:
        Sum of the two numbers
    """
    return n1 + n2
```

### Adding Dependencies

```bash
# Add runtime dependency
uv add package-name

# Add development dependency
uv add --dev package-name

# Update lockfile
uv sync --dev
```

### Environment Variables

Create a `.env` file in the project root for local development (not committed to git):

```bash
OTEL_SERVICE_NAME=fastapi-app
OTEL_SERVICE_INSTANCE_ID=local-dev
```

## Pre-commit Hooks

The project uses pre-commit hooks (configured in `.pre-commit-config.yaml`):

```bash
# Install hooks
pre-commit install

# Run manually on all files
uv run poe pre-commit-run

# Run on staged files (automatic on commit)
git commit -m "Your message"
```

Hooks automatically:

- Check YAML formatting
- Detect merge conflicts
- Check for large files
- Validate conventional commit messages
- Run Ruff linter and formatter
- Update lockfile with uv

## Debugging

### Python Debugging

```bash
# Run with Python debugger
python -m pdb src/pyproject_template/main.py

# Or add breakpoint in code
breakpoint()  # Stops execution in debugger
```

### FastAPI Debugging

Access interactive docs:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Type Checking Issues

Run type checker for detailed error messages:

```bash
uv run poe type-check
```

## Performance Profiling

```bash
# CPU profiling with cProfile
python -m cProfile -s cumtime src/pyproject_template/main.py

# Memory profiling (requires memory-profiler)
uv add --dev memory-profiler
python -m memory_profiler src/pyproject_template/main.py
```

## Troubleshooting

### Tests Not Found

Ensure test files follow naming convention: `test_*.py` or `*_test.py` in `src/tests/` directory.

### Import Errors

```bash
# Verify package installation
uv sync --dev

# Check Python path
python -c "import sys; print(sys.path)"
```

### Coverage Too Low

```bash
# See detailed coverage report
uv run poe test-cov
# Then check htmlcov/index.html
```

### Pre-commit Hook Failures

```bash
# See which hooks are failing
uv run poe pre-commit-run

# Fix issues and try again
uv run poe lint format
git add .
git commit -m "fix: address linting issues"
```

## Continuous Integration

The project uses GitHub Actions for CI/CD (configured in `.github/workflows/`):

- **checks.yml**: Code quality checks (linting, formatting, type checking)
- **cicd.yml**: Tests and coverage reporting

All checks must pass before merging PRs.

## Contributing Guidelines

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.
