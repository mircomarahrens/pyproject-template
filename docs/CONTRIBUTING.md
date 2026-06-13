# Contributing

Thank you for your interest in contributing to this project! We welcome contributions of all kinds.

## Code of Conduct

Please be respectful and constructive in all interactions.

## Getting Started

1. **Fork and clone** the repository:

   ```bash
   git clone https://github.com/your-username/pyproject-template.git
   cd pyproject-template
   ```

2. **Set up your development environment**:

   ```bash
   uv sync --dev
   ```

3. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Workflow

### Code Quality Standards

All code must pass:

- **Linting**: `uv run poe lint`
- **Formatting**: `uv run poe format`
- **Type checking**: `uv run poe type-check`
- **Tests**: `uv run poe test`

### Running Quality Checks

Before committing, run all checks:

```bash
uv run poe check
```

### Writing Tests

- Place tests in `src/tests/`
- Use test naming convention: `test_*.py` or `*_test.py`
- Mark tests with appropriate markers:
  
  ```python
  import pytest
  
  @pytest.mark.unit
  def test_something():
      assert True
  
  @pytest.mark.integration
  def test_integration():
      assert True
  ```

### Coverage Requirements

Minimum coverage threshold is **70%**. Check coverage:

```bash
uv run poe test-cov
```

## Commit Message Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/):

```txt
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Types:**

- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, missing semicolons, etc.)
- `refactor`: Code refactoring without feature changes
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Build process, dependencies, etc.
- `ci`: CI/CD configuration changes

**Example:**

```txt
feat(api): add new endpoint for user authentication

Implemented JWT-based authentication with token refresh mechanism.
Added comprehensive test coverage for auth endpoints.

Closes #123
```

## Pull Request Process

1. **Ensure all tests pass**: `uv run poe test-cov`
2. **Keep commits atomic and well-documented**: Use conventional commit messages
3. **Write a clear PR description** explaining:
   - What changes were made
   - Why they were made
   - How to test the changes
4. **Link to related issues**: Use GitHub keywords like `Closes #123`

## Documentation

- Update relevant documentation files when changing functionality
- Keep README.md up-to-date
- Add docstrings to new functions and classes
- Build documentation locally to verify:

  ```bash
  uv run poe docs-build
  uv run poe docs-serve
  ```

## Reporting Issues

When reporting issues, please include:

- Python version
- Operating system
- Steps to reproduce
- Expected behavior
- Actual behavior
- Any relevant error messages or logs

## Questions?

Feel free to open a discussion or issue if you have questions!
