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

- Python 3.8+ (CI runs 3.10 and 3.13)
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

A plain `pytest` never signs in: live suites are opt-in with `--live`, because they
write to a real tenant. This runs the offline suites and is what CI runs on Python 3.10
and 3.13. It is the fastest way to validate a change, and where new tests should go.

The offline tests are split by what they describe:

| Directory | Subject |
| --- | --- |
| `tests/unit` | the shipped library — one file per feature of `office365`, plus `test_regressions.py` for the pins that are one assertion long |
| `tests/tooling` | the code generator under `generator/`, which is development tooling and is not part of the wheel |
| `tests/test_settings.py` | the `tests/settings.py` configuration loader and its `.env` grammar |
| `tests/test_setup.py` | the `tests/setup.py` wizard's decisions (offline, `-y`, no prompts) |
| `tests/test_capabilities.py` | the declared-permission vocabulary: checking, skipping and reporting |

The bootstrap itself has one module per job, and nothing else: `tests/settings.py`
resolves configuration (`Settings`, the `.env` file, readiness), `tests/setup.py`
provisions it (the interactive wizard is the only writer of `.env`), `tests/doctor.py`
reports it, and `tests/preflight.py` reports what the *live suites* still need from the
tenant (permissions, roles, licenses) — see below. A value is spelled once — in the `Settings` dataclass —
and the legacy `tests.site_url` / `tests.test_site_url` spellings are a `__getattr__`
over its fields, not a list to keep in step.

A test belongs in `tests/unit` when it pins behaviour a user of the library can
observe; it belongs in `tests/tooling` when it pins how the library is generated. A
generator file is named after the module it drives, and holds both halves of that module's
subject: the keys plan and the write it feeds (`@key(...)`), the beta gate and the write it
feeds (`@version(beta=...)`), the import block and the helpers that insert into it. A
17-line test of `BuilderContext` is not a file; it is the last section of the config file
that builds one.

### A live test declares what it needs from the tenant

A credentialed test that needs more than credentials says so next to itself, and the
declaration is the only place the requirement is written:

```python
@requires_delegated("Mail.Read", bypass_roles=["Global Administrator"])
def test_01_list_messages(self): ...
```

`tests/decorators.py` stamps the requirement on the test it returns, so
`tests/preflight.py` can read the whole matrix off the test tree without running
anything — `python -m tests.preflight` needs no credentials, `--verify` resolves each
requirement against the signed-in app and user, and `--report tests-report` writes
`preflight.md` (add `--json tests-report` for `preflight.json`). Both the guard and the
report call the same `tests/capabilities.py`, where a `Requirement` answers
`unmet(state)` and `TenantState` fetches *only* the facts the requirement names — an
app-only token has no `/me` to ask for licenses, so asking would turn a skip into a
failure.

`python -m tests.setup --grant` turns that matrix into the *smallest* set of grants that
would unblock the tree: one name per any-of group, shared names asked for once, a
confirmation before anything changes, and a re-read of the tenant afterwards. A
requirement this wizard cannot satisfy — a directory role for the test user, a license
that has to be bought — is named rather than dropped.

A permission the tenant does not grant must be visible in three places, and all three
read from the same object: the skip reason (`missing delegated: any of Mail.Read`), the
`pytest` summary (`N  delegated: any of …`), and the report file. Add the requirement
to the test, not to a list in the report.

Within a file, a test also has to earn its place: it must execute a line, or make
an assertion, that no other test in that file makes. Where a richer test already
walks the same lines and asserts the same facts, the narrower one is deleted rather
than kept beside it. The suite was halved on that measure — 2,233 collected tests
became 1,113, while the lines exercised by `office365/` moved from 16,937 to 16,383
(3.3%): the other 47% of the tests were re-walking covered ground. The measurement
is reproducible with `coverage run --contexts` over the suite and a set-cover over
`(test → lines, assertions)`; it is not a matter of taste.

A second pass asked a different question: does `tests/<product>/` already pin this
fact against a live tenant? Those suites cannot run here without credentials, so
the answer is argued from the E2E file's subject, paths and verbs — never from a
run. What a live suite already pins (a request shape, a payload spelling, a tour
of accessors) is deleted here; what it cannot pin offline stays — error typing,
the exact bytes emitted, canonical checksums, and the rules the client derives
before it ever sends a request. That pass took 1,112 tests to 812 and the
statements `office365/` executes from 53,659 to 52,500 (2.2%).

A third pass took the same criterion to its end. Eight files were about the
exchange and nothing else — the two transport adapters, the `client-request-id`
header, the batch envelope, the paging loop, and the streaming and chunked
transfer loops — and every one of them pinned a shape a product suite already
walks against a tenant: `tests/sharepoint/test_client.py` submits batches,
`tests/sharepoint/test_large_list.py` pages a list, `tests/sharepoint/test_file.py`
streams a large file up and down through the same transport. They are gone:
77 tests and 2,001 lines. What stayed is what a tenant cannot script — a 429
with a `Retry-After`, a 202 that polls through seven fractions, an awaitable
token callback, a tolerant write, an idempotent ensure — because no run against
a live service can provoke those on demand, and a fake is the only stimulus that
reaches the branch.

A fourth pass asked who each test is for. A pin that is one assertion long — a getter
that read a neighbour's wire name, a body that spelled `+00:00` where the service takes
`Z`, a private `_certificate_der` on its own — was spending twenty lines of docstring,
imports and a helper on one `assert`. Twenty-seven such files became one
`tests/unit/test_regressions.py`, grouped by the kind of mistake and commented one line
each; the near-duplicates they had grown (`test_prefer.py`'s three header variants,
`test_enum_flags.py`'s four reads of one `parse_enum` call) were merged. What went with
them were tests that graded the harness instead of the library: the limits registry's
identity bookkeeping, the docs generator's scanner, and the self-check that
`make_dataclass` rejects an unhashable default on the interpreter running the suite. A
ratchet's job is to fail on this tree; feeding it a synthetic offender tests the
interpreter.

A fifth pass asked whether a fake payload for a real endpoint earns its keep.
`test_comparable_profile.py` spelled out one comparison rule at a time — 25 tests whose
subject is the digest the migration engine computes, not the service — and it duplicated a
property two other files already hold: `test_calendar_profile.py` pins the digest of an
event's canonical form and what gating a field does to it, and the declaration ratchet pins
that every rule fits its field. `test_content_type_links.py` asserted a request body one
assertion long. Both are gone, as is a download test whose async terminal re-walked its own
sync twin (async dispatch has its own file). What stayed is what no run against a tenant
provokes: a download that resumes a partial file, and a feature activation whose `GetById`
answers `null` for every feature at site scope — the end-to-end activation test is
idempotent, so on a tenant where the feature is already active it passes even when the
client suppresses the write.

A sixth pass went after the fakes rather than the assertions. The cost of a
double-heavy file is the double, not the test: `test_sharepoint_library_target.py` spent
369 of its 640 lines on stand-ins for `File`, `Folder`, `ListItem` and the web, so the
tests were asserting against a model of the library instead of the library. It now builds
a real `ClientContext` over a `RoutingTransport` and scripts only the service's answers —
404 lines, and one test more than before, because the request path the doubles had
screened is now visible (`Files/add(overwrite=true,url='a.txt')`, no folder ensure). The
rule: **a fixture may be a wire envelope; it must never hand-copy a model's shape.** A
202 with a `Location` header, a `{"d": {"results": []}}` page, a `#microsoft.graph.driveItem`
body — those are the service speaking, and they belong in `tests/_scripted_transport.py` as
a payload. A stand-in for `File` that answers `get_property()` is the library speaking to
itself, and it pins whatever the stand-in does, not what the library does. Mocking a
`TeamsOperation` to assert the operation's own parse is the limiting case: the payload
would be asserting itself. Doubles that survive all read client-side state a payload
cannot carry — a thread's name, two requests in flight at once, a digest handshake.

That file also ended 17 copies of the same transport. `tests/_scripted_transport.py` now
exports `RecordingTransport` (payloads in call order, plus the requests received) beside
`ScriptedTransport` and `RoutingTransport`; the clones in the product test files were
byte-for-byte the same eleven lines, 13 of them replaced. If a test needs a transport that
does something new, the something new belongs in the shared module, where the next test
finds it instead of writing their own.

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
