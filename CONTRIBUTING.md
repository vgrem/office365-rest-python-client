# Welcome Contributors! 🎉

Thank you for your interest in contributing to the `office365-rest-python-client` library. This project provides a comprehensive Python client for Microsoft 365 and Microsoft Graph APIs.

> **No Microsoft 365 tenant is needed to contribute code.** `uv run pytest -q`
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

- Python 3.10+ (CI tests 3.10 through 3.14; the lockfile and dev tooling need 3.11+)
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
uv run pytest -q
```

A plain `pytest` never signs in: live suites are opt-in with `--live` (or
`OFFICE365_LIVE=1` in `.env`, which is how an IDE's test runner gets one), because they
write to a real tenant. This runs the offline suites and is what CI runs on Python 3.10
to 3.14. It is the fastest way to validate a change, and where new tests should go.

The offline tests are split by what they describe:

| Directory | Subject |
| --- | --- |
| `tests/unit` | the shipped library — one file per feature of `office365`, plus the whole-tree coherence walks; the command line is one file, `tests/unit/test_cli.py` |
| `tests/tooling` | the code generator under `generator/` — CSDL in, source out: one end-to-end run, staged |
| `tests/unit/test_permissions.py` | the declared-permission vocabulary: what the tree declares, and what a test does with it |

The bootstrap itself has one module per job, and nothing else: `tests/settings.py`
resolves configuration (`Settings`, the `.env` file, readiness), `tests/doctor.py`
reports it, and `tests/preflight.py` reports what the *live suites* still need from the
tenant (permissions, roles, licenses) and can grant it with `--grant` — nothing in the
repo writes `.env`, and the example scripts print the two values a tenant reveals once.
See below. A value is spelled once — in the `Settings` dataclass —
and the legacy `tests.site_url` / `tests.test_site_url` spellings are a `__getattr__`
over its fields, not a list to keep in step.

A test belongs in `tests/unit` when it pins behaviour a user of the library can
observe; it belongs in `tests/tooling` when it pins how the library is generated. The
generator is a development tool — nobody imports it, nobody holds its API — so `tests/tooling`
keeps only what a wrong change would break silently:

`test_generator_e2e.py` hands a small CSDL document to the v3 and the v4 reader and
follows one run through its steps, a test per step: the document read into the type model
(keys, members, navigations, bound operations), an EDM type becoming its Python type, the
model rendered as entity, complex and enum classes, and a second run against changed
metadata — what was gained is written, what a person wrote stays, what was dropped is
reported and kept in code. Every generated module is `ast.parse`d.

The builders' individual decisions (how a name is snake-cased, how a type is mapped) are
not pinned one by one: a regression there shows up in the end-to-end run, and a test of a
private helper costs more to maintain than the bug it prevents.

### A live test declares what it needs from the tenant

A credentialed test that needs more than credentials says so next to itself, and the
declaration is the only place the requirement is written:

```python
@requires_delegated("Mail.Read", bypass_roles=["Global Administrator"])
def test_01_list_messages(self): ...
```

`tests/decorators.py` stamps the requirement on the test it returns — and, for
`@requires_call`, the model methods it was derived from — so `tests/preflight.py` reads the
whole matrix off the test tree without running anything. `python -m tests.preflight` needs no
credentials, and `--verify` resolves each requirement against the signed-in app and user.
The console summary, guard, and decorators use the same `tests/capabilities.py`,
where a `Requirement` answers `unmet(state)` and `TenantState` fetches *only* the facts the
requirement names — an app-only token has no `/me` to ask for licenses, so asking would turn
a skip into a failure.

`python -m tests.preflight --grant` turns that matrix into the *smallest* set of grants that
would unblock the tree: one name per any-of group, shared names asked for once, a
confirmation before anything changes, and a re-read of the tenant afterwards. A
requirement it cannot satisfy — a directory role for the test user, a license
that has to be bought — is named rather than dropped.

A permission the tenant does not grant must be visible in three places, and all three
read from the same object: the skip reason (`missing delegated: any of Mail.Read`), the
`pytest` summary (`N  delegated: any of …`), and the console preflight summary. Add the
requirement to the test, not to a separate list.

### What a test is worth

Within a file, a test has to earn its place: it must execute a line, or make an
assertion, that no other test in that file makes. Where a richer test already walks the
same lines and asserts the same facts, the narrower one is deleted rather than kept
beside it. The suite was halved on that measure — 2,233 collected tests became 1,113,
while the lines exercised by `office365/` moved from 16,937 to 16,383 (3.3%): the other
47% of the tests were re-walking covered ground. The measurement is reproducible with
`coverage run --contexts` over the suite and a set-cover over `(test → lines,
assertions)`; it is not a matter of taste.

A live suite pins the request a method sends and the payload it parses, so an offline
test that re-walks a covered path goes with it. What stays offline is what no run
against a tenant can provoke or observe: error typing, the exact bytes emitted, a
canonical checksum, a rule the client derives before it ever sends a request, a 429 with
`Retry-After`, a 202 that polls, an awaitable token callback, a tolerant write, an
idempotent ensure, a download that resumes a partial file.

Three kinds of pin are not worth the file they live in. A pin one assertion long — a
getter that read a neighbour's wire name, a body that spelled `+00:00` where the service
takes `Z` — costs more in imports and a helper than the bug it prevents: put it in the
file that owns the subject, or delete it. A pin under a comment naming a closed defect is
a changelog in code, and never fails for a reason a reader can act on. And a test that
grades the harness or the interpreter — a ratchet fed a synthetic offender,
`make_dataclass` rejecting an unhashable default — tests Python, not this library.

Ask of every file whether its subject is a *decision* or the way the decision is spelled:
the XML a builder emits, how a debugging aid prints, how a third-party bridge round-trips
— each is already covered by the suite that walks the same path through the same code.

#### A fixture is a wire envelope, not a stand-in model

**A fixture may be a wire envelope; it must never hand-copy a model's shape.** A 202 with a
`Location` header, a `{"d": {"results": []}}` page, a `#microsoft.graph.driveItem` body —
those are the service speaking, and they belong in `tests/_scripted_transport.py` as a
payload. A stand-in for `File` that answers `get_property()` is the library speaking to
itself: it pins whatever the double does, not what the library does, and mocking an
operation to assert that operation's own parse is the limiting case where the payload
asserts itself. Build a real `ClientContext` over a transport and script only the service's
answers: the request path stays visible, which is half of what the test is for. A double
survives only where it reads client-side state a payload cannot carry — a thread's name,
two requests in flight at once, a digest handshake.

`tests/_scripted_transport.py` holds every transport the suite scripts — `ScriptedTransport`
and its `RecordingTransport` variant (payloads in call order, plus the requests received),
`RoutingTransport`, and the async and method-routing ones. A test that needs a transport
doing something new adds it there, where the next test finds it instead of writing another
copy.

### End-to-end tests (maintainers / optional)

The product suites (`tests/sharepoint/`, `tests/onedrive/`, …) are end-to-end and
need real Microsoft 365 credentials. The full setup — `.env` template, the authentication flows, certificate
generation, required tenant roles and troubleshooting — lives in
[README-dev.md](README-dev.md). In short:

```bash
cp .env.example .env
uv run python -m tests.doctor
uv run pytest tests/sharepoint/
```

Credentials are loaded automatically from `.env`, so no `export` is needed. Live
tests with unconfigured credentials are skipped, not failed.

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
3. Ensure the offline checks pass (`ruff`, `pyright`, `pytest`)

### Pull Request Process

1. CI checks must pass:
   - Ruff linting and formatting
   - Pyright
   - Offline unit tests (`pytest`)
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
