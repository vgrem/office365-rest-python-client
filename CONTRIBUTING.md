# Welcome Contributors! 🎉

Thank you for your interest in contributing to the `office365-rest-python-client` library. This project provides a comprehensive Python client for Microsoft 365 and Microsoft Graph APIs.

> **No Microsoft 365 tenant is needed to contribute code.** `uv run pytest --offline -q`
> runs the unit suite offline — it's exactly what CI runs. Use it to validate your
> change; maintainers run the credentialed end-to-end suite.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Development Environment Setup](#development-environment-setup)
3. [Code Style and Quality Standards](#code-style-and-quality-standards)
4. [Testing Guidelines](#testing-guidelines)
5. [Finding Something to Work On](#finding-something-to-work-on)
6. [Submitting Changes](#submitting-changes)
7. [Issue Reporting](#issue-reporting)
8. [Documentation](#documentation)
9. [Community Guidelines](#community-guidelines)

## Getting Started

### Prerequisites

- Python 3.8+ (CI runs 3.8, 3.10 and 3.13)
- Git
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Microsoft 365 tenant is **recommended but not required** — most contributions
  can be validated with the offline unit suite

### Fork and Clone

1. Fork the repository on GitHub
2. Clone your fork locally:

```bash
git clone https://github.com/your-username/office365-rest-python-client.git
cd office365-rest-python-client
```

## Development Environment Setup

Install dependencies (including all optional extras used by the tests):

```bash
uv sync --all-extras
```

### Pre-commit hooks (recommended)

The hooks run `pyproject-fmt`, `uv lock`, `ruff`, `pyright` and `pytest`:

```bash
uv tool install prek
prek run --all-files
```

## Code Style and Quality Standards

The project uses the following tools (mirroring CI):

- [Ruff](https://docs.astral.sh/ruff/) — linting, import sorting and formatting
- [Pyright](https://microsoft.github.io/pyright/) — static type checking

Line length is 121 characters (configured in `pyproject.toml`).

Run the same checks locally before pushing:

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pyright
```

## Testing Guidelines

### Offline unit tests (no tenant required)

```bash
uv run pytest --offline -q
```

This runs `tests/unit` fully offline and is what CI runs on Python 3.8, 3.10 and 3.13.
It is the fastest way to validate a change, and where new tests should go.

### End-to-end tests (maintainers / optional)

The `tests/` suites outside `tests/unit` are end-to-end and need real Microsoft 365
credentials. If you have a tenant, create a `.env` file in the project root (it is
`.gitignore`d):

```bash
OFFICE365_TENANT=contoso.onmicrosoft.com
OFFICE365_CLIENT_ID=00000000-0000-0000-0000-000000000000
OFFICE365_CLIENT_SECRET=...
OFFICE365_USERNAME=admin@contoso.onmicrosoft.com
OFFICE365_PASSWORD=...
# optional — derived from OFFICE365_TENANT when omitted
OFFICE365_TENANT_PREFIX=contoso
OFFICE365_TEAM_SITE_URL=https://contoso.sharepoint.com/sites/project
OFFICE365_ADMIN_SITE_URL=https://contoso-admin.sharepoint.com
```

`tests/settings.py` reads these variables and loads `.env` automatically, so no
`export` is needed:

```bash
uv run pytest tests/sharepoint/
```

`OFFICE365_TENANT`, `OFFICE365_CLIENT_ID`, `OFFICE365_CLIENT_SECRET`,
`OFFICE365_USERNAME` and `OFFICE365_PASSWORD` are mandatory; the rest are optional
and only needed for specific scenarios.

#### Required tenant permissions

For comprehensive testing, your test tenant should have these admin roles:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin

#### Forks and CI

- Forked pull requests do not receive repository secrets, so the credentialed
  tests are skipped automatically; formatting, linting, type checking and the
  offline unit suite still run.
- Maintainers run the full E2E suite on branches with secrets before merging.
- The scheduled `Integration Tests` workflow reads one repository secret,
  `OFFICE365_ENV`, which holds the full `.env` contents, and writes it to `.env`
  before running `pytest`.

## Finding Something to Work On

- Browse issues labeled [`good first issue`](https://github.com/vgrem/office365-rest-python-client/labels/good%20first%20issue)
  (small, well-scoped) and [`help wanted`](https://github.com/vgrem/office365-rest-python-client/labels/help%20wanted).
- Add or improve tests under `tests/unit` — a failing test with a clear reproduction
  is one of the most valuable contributions.
- Improve the examples under `examples/` or the docs.
- Not sure where to start? Ask in
  [Discussions](https://github.com/vgrem/office365-rest-python-client/discussions).

## Submitting Changes

### Branching Strategy

1. Create a feature branch from `master`:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes with clear, focused commits
3. Ensure the offline checks pass (`ruff`, `pyright`, `pytest --offline`)

### Pull Request Process

1. CI checks must pass:
   - Ruff linting and formatting
   - Pyright
   - Offline unit tests (`pytest --offline`)
   - Documentation build (`mkdocs build --strict`) when docs/examples change
2. Await maintainer review
3. Update documentation and examples where applicable

### Commit Guidelines

- Use clear, descriptive commit messages
- Reference issue numbers when applicable
- Keep commits focused and atomic

## Issue Reporting

Before filing an issue:

1. Search existing issues
2. Check the documentation and examples
3. Test with the latest version

Include in your report:

- Environment: Python version, OS, library version
- Reproduction: minimal code example
- Expected vs actual behavior
- Authentication method used
- Targeted service area (SharePoint, Graph, etc.)

## Documentation

### API Coverage

The library supports multiple Microsoft 365 APIs, including SharePoint REST,
Microsoft Graph, OneDrive, Outlook, Teams, OneNote, and Planner. See `examples/`
for usage.

### Building the docs

The site (MkDocs + Material) is generated from the package docstrings and every
script under `examples/`. Validate with `--strict` before pushing:

```bash
uv sync --group docs
uv run mkdocs serve        # local preview at http://127.0.0.1:8000
uv run mkdocs build --strict
```

`mkdocs build --strict` fails on any example that is not valid Python or on a
`README.md` link pointing to a missing file. The site deploys to GitHub Pages on
every push to `master` via `.github/workflows/pages.yml`.

## Community Guidelines

This project is maintained by volunteers. Contributions are welcome but never
required, and there is no service-level agreement — issues and pull requests are
triaged as time allows.

Sponsorship is entirely optional; the library stays free and MIT-licensed. It is
appreciated and never affects whether an issue is fixed. See the Support section
of the [README](README.md) if you'd like to help fund maintenance.

Be respectful and constructive in all interactions.

### Maintainer automation

Issue triage is automated by the `office365-maintainer` GitHub App, which posts
as [`office365-maintainer[bot]`](https://github.com/apps/office365-maintainer).
Maintainers can drive it with a slash-command in an issue comment:

| Command | Effect |
| --- | --- |
| `/close` | Close the issue with a canned reply |
| `/reopen` | Reopen the issue |
| `/duplicate #123` | Link as a duplicate, then close |
| `/label <name>` | Add an existing label to the issue |

Commands are honored only for comments from `OWNER`, `MEMBER` or `COLLABORATOR`
accounts, and the triggering command comment is deleted afterwards so the thread
only shows the bot's action (see `.github/workflows/maintainer.yml`).

To perform manual actions under the same bot identity, export a short-lived
installation token and use `gh` as usual:

```bash
export GH_TOKEN="$(uv run python scripts/github_app_token.py \
    --app-id <app-id> \
    --private-key ~/.config/office365-maintainer/app.pem \
    --repo vgrem/office365-rest-python-client)"
gh issue comment 123 --body-file reply.md
```

The token expires after about an hour; re-run the command to refresh it. `git`
operations are unaffected and still use your own identity.

### License

MIT License. By contributing, you agree that your contributions are licensed under
these terms.
