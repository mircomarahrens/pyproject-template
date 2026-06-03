# Welcome to the Pyproject Template repository

This is a template for Python projects. It can be used as a starting point for
new Python projects.

This template is based on the Python packaging and dependency management tool
[uv](https://docs.astral.sh/uv/). The central file for project management in
uv is the file `pyproject.toml`.

## Best practices with Git

```bash
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
# if you have to deal with multiple git accounts you can use something like:
[includeIf "gitdir:~/github/privategit"]
    path = ~/github/privategit/.gitconfig
```

The file `~/.gitmessage` is used as a template for commit messages. Our file
here looks like this:

```bash
$ cat .gitmessage
<type>[optional scope]: <description>
# Following <https://www.conventionalcommits.org/en/v1.0.0/>
# <type>[optional scope]: <description>
#
#
# [optional body]
#
# [optional footer(s)]
#
# The commit contains the following structural elements, to communicate intent to the consumers of your library:
#
# 1. fix: a commit of the type fix patches a bug in your codebase (this correlates with PATCH in Semantic Versioning).
# 2. feat: a commit of the type feat introduces a new feature to the codebase (this correlates with MINOR in Semantic Versioning).
# 3. BREAKING CHANGE: a commit that has a footer BREAKING CHANGE:, or appends a ! after the type/scope, introduces a breaking API change (correlating with MAJOR in Semantic Versioning). A BREAKING CHANGE can be part of commits of any type.
# 4. types other than fix: and feat: are allowed, for example @commitlint/config-conventional (based on the Angular convention) recommends build:, chore:, ci:, docs:, style:, refactor:, perf:, test:, and others.
# 5. footers other than BREAKING CHANGE: <description> may be provided and follow a convention similar to git trailer format.
#

```

The content after `#` are comments and are ignored by git.

## Project

### Pre-dependencies

- [Poetry (Python Packaging and Dependency Management)](https://python-poetry.org/)
- [Pre-Commit (Managing the pre-commit Git hook)](https://pre-commit.com/)

### Getting started

Run from the root directory of this repository (actually where the
'pyproject.toml' is located)

```bash
uv sync
```

To start the virtual environment run

```bash
source .venv/bin/activate
```

To stop the virtual environment run

```bash
deactivate
```

### Unittesting via `pytest`

To check if the envrionment is set up correctly run `pytest`, like

```bash
> pytest
========================= test session starts ==========================
platform linux -- Python 3.11.13, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/mircomarahrens/github/mircomarahrens/pyproject-template
configfile: pyproject.toml
plugins: anyio-4.12.1, cov-7.0.0, mock-3.15.1
collected 2 items

tests/app_test.py .                                              [ 50%]
tests/server_test.py .                                           [100%]

========================== 2 passed in 0.69s ===========================
```

Your output should be similiar to the above output. One test is failing on
purpose.

#### Coverage testing with `pytest-cov`

```bash
> pytest --cov
========================= test session starts ==========================
platform linux -- Python 3.11.13, pytest-9.0.2, pluggy-1.6.0
rootdir: /home/mircomarahrens/github/mircomarahrens/pyproject-template
configfile: pyproject.toml
plugins: anyio-4.12.1, cov-7.0.0, mock-3.15.1
collected 2 items

tests/app_test.py .                                              [ 50%]
tests/server_test.py .                                           [100%]

============================ tests coverage ============================
___________ coverage: platform linux, python 3.11.13-final-0 ___________

Name                     Stmts   Miss  Cover
--------------------------------------------
python/__init__.py           0      0   100%
python/api/__init__.py       0      0   100%
python/api/main.py          34     10    71%
python/arithmetic.py         2      0   100%
tests/__init__.py            0      0   100%
tests/app_test.py            3      0   100%
tests/server_test.py         7      0   100%
--------------------------------------------
TOTAL                       46     10    78%
========================== 2 passed in 1.53s ===========================
```

### Serving restful APIs via `fastapi`

You can find in the file `api/server.py` some basic code to serve restful APIs
via [FastAPI](ttps://fastapi.tiangolo.com/). To start the server simply run

```bash
> fastapi dev api/server.py
INFO     Using path api/server.py
INFO     Resolved absolute path /Users/mircomarahrens/Projects/pyproject-template/api/server.py
INFO     Searching for package file structure from directories with __init__.py files
INFO     Importing from /Users/mircomarahrens/Projects/pyproject-template

 ╭─ Python package file structure ─╮
 │                                 │
 │  📁 api                         │
 │  ├── 🐍 __init__.py             │
 │  └── 🐍 server.py               │
 │                                 │
 ╰─────────────────────────────────╯

INFO     Importing module api.server
INFO     Found importable FastAPI app

 ╭─── Importable FastAPI app ───╮
 │                              │
 │  from api.server import app  │
 │                              │
 ╰──────────────────────────────╯

INFO     Using import string api.server:app

 ╭────────── FastAPI CLI - Development mode ───────────╮
 │                                                     │
 │  Serving at: http://127.0.0.1:8000                  │
 │                                                     │
 │  API docs: http://127.0.0.1:8000/docs               │
 │                                                     │
 │  Running in development mode, for production use:   │
 │                                                     │
 │  fastapi run                                        │
 │                                                     │
 ╰─────────────────────────────────────────────────────╯

INFO:     Will watch for changes in these directories: ['/Users/mircomarahrens/Projects/pyproject-template']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [11520] using WatchFiles
INFO:     Started server process [11522]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

FastAPI provides a Swagger-UI. Visit <http://127.0.0.1:8000/docs> to see it.
Shutdown the server via <CTRL+C>.

### Pre-commit

To install the pre-commit hooks run the following command

```bash
> pre-commit install
```

To manually run the pre-commit hooks run the following command

```bash
> pre-commit run --all-files
```

### Linting

We are using [Ruff](https://github.com/astral-sh/ruff) for linting. Ruff is a
linter and formatter for Python code. Ruff uses
[rules](https://docs.astral.sh/ruff/rules/) which are based on style guides
([Pep8](https://peps.python.org/pep-0008/) is the root of those style guides).
The rules are defined in the file `pyproject.toml` under the section
`[tool.ruff.rules]`. One can explicit include or exclude rules, like

```toml
[tool.ruff.lint]
select = [
    "E", # pycodestyle
    "W", # pycodestyle
    "F", # Pyflakes
    "B", # flake8-bugbear
    "PIE", # flake8-pie
    "C4", # flake8-comprehensions
    "I", # isort
    "UP", # pyupgrade
]
ignore = ["E501","E203","B024","B028","UP037"]
```

We are using the rule convention used by Netflix in their
[Iceberg Python project](https://github.com/Netflix/iceberg-python/blob/main/ruff.toml).
To specify on which file types Ruff is running on use the key ´types_or´ in the
pre-commit hook. See
[ruff-pre-commit](https://github.com/astral-sh/ruff-pre-commit) for details.

### Mkdocs

Run the following command to serve the documentation locally:

```bash
> uv run mkdocs serve
```

To build the static site for your documentation, run:

```bash
> uv run mkdocs build
```

### Podman

The given Dockerfile is a multi-stage build. The first stage is the build stage
(named `base` here) and the second stage (named `dev` here) is a runtime stage
for development. The build stage is used to install the dependencies and build
the Python package. The runtime stage is used to run the Python package. To
build the Podman image and target the dev stage run the following command:

```bash
podman build -t pyproject-template . --target python-dev --no-cache
```

Initially, the Podman image is built with the base and the dev stage. Afterwards
only the dev stage is rebuilt. The flag `--no-cache` in this case is used to
avoid caching the dev stage.

To run the Podman container run the following command:

```bash
podman run -p 8080:8080 pyproject-template
```

### Podman compose

This project provides a `compose.python.yaml` that also works with Podman's
compose implementation. The examples below show common workflows for
development and cleanup.

Prerequisites:

- `podman` (v3+ recommended) with the `podman compose` subcommand available.
- A running container registry if you push/pull images (optional for local builds).

Start development containers (detached):

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml up -d
```

Stop and remove containers:

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml down
```

Useful commands while running:

- View logs: `podman compose -f compose.python.yaml -f compose.python.dev.yaml logs -f <service>`
- List containers: `podman ps -a`
- Exec into a container: `podman exec -it <container> /bin/sh` (or `/bin/bash`)
- Remove unused images: `podman image prune -a`

### Troubleshooting

If you cannot login into OpenObserve:

```bash
podman compose -f compose.python.yaml -f compose.python.dev.yaml down -v # remove also volumes
```

Restart the containers again.

Afterwards you need to reset the value for `OPENOBSERVE_AUTH_KEY` in the
`compose.python.dev.yaml` file to the correct value. You can find the correct value
in the OpenObserve UI under "Data Sources" -> "Security".

Shut down the containers and restart them again to pull the correct auth key.

## Branching strategy

We are following the [trunked-based development](https://www.atlassian.com/continuous-delivery/continuous-integration/trunk-based-development).

The default branch is `main`. This branch serves as the single source of truth
for all environments: development (dev), acceptance (acc), and production (prd).

- **Development Environment**: Changes are deployed to the development
  environment by directly pushing to the `main` branch. This ensures that the
  latest updates are always available for testing and iteration.

- **Acceptance Environment**: Deployment to the acceptance environment is
  triggered by creating a pre-release, also known as a release candidate. This
  step allows for thorough validation and testing before the final release.

- **Production Environment**: Deployment to the production environment is
  initiated by creating a release. This marks the final, stable version of the
  software, ready for end-users.

This streamlined approach ensures a clear and efficient workflow, minimizing
merge conflicts and simplifying the release process.
