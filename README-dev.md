# Local development

Run the tests and the runnable examples in `examples/` on your machine.

## Install

```bash
git clone https://github.com/vgrem/office365-rest-python-client.git
cd office365-rest-python-client

uv venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
uv sync --all-extras
```

Using `pip`: `python3 -m venv venv && source venv/bin/activate && pip install -e ".[examples,ntlm]" pytest`

## Run offline tests (no tenant)

```bash
uv run pytest -q
```

Offline is the default: a bare `pytest` cannot reach a tenant. Add `--live` to also run
what the credentials in `.env` make reachable (slow, and it writes to the tenant).

That is the whole setup for most contributions. Continue only to run against a real tenant.

## Lint, format and git hooks

Install the git hooks once per clone:

```bash
uv run pre-commit install
```

That single command registers both stages:

- **commit** — `pyproject-fmt`, `uv lock`, and `ruff check --fix` / `ruff format` on the
  files you staged (fast).
- **push** — `pyright` and the offline test suite, `uv run pytest` (slower).

Run everything against the whole tree without committing:

```bash
uv run pre-commit run --all-files
uv run pre-commit run --hook-stage pre-push --all-files
```

The hooks invoke the tools from the locked environment, and CI installs the same
lockfile, so the versions you run locally match the ones that gate the build.

---

## Set up live authentication

Credentials live in one `.env` at the repo root (loaded automatically, nothing to
`export`). Verify what is configured at any time:

```bash
uv run python -m tests.doctor
```

### 1. Create `.env`

```bash
cp .env.example .env
```

### 2. Register app in Entra (manual)

[Register an app](https://learn.microsoft.com/entra/identity-platform/quickstart-register-app),
then fill in the tenant, client ID and an admin account:

```dotenv
OFFICE365_TENANT=contoso.onmicrosoft.com
OFFICE365_CLIENT_ID=00000000-0000-0000-0000-000000000000
OFFICE365_ADMIN_USERNAME=admin@contoso.onmicrosoft.com
```

The admin needs **Global Administrator**, **Privileged Role Administrator** or
**Application Administrator**.

### 3. Grant permissions

Once `.env` exists, the wizard can grant everything the live suites declare and the
tenant lacks — it reads the requirement matrix, prints the plan, asks, grants, and
re-reads the tenant (see [Grant what the suites need](#grant-what-the-suites-need)):

```bash
uv run python -m tests.setup --grant --dry-run   # see the plan first
uv run python -m tests.setup --grant             # grant it
```

For a single permission, the two scripts below take a name and apply admin consent:

```bash
uv run python examples/entraid/applications/grant_application_perms.py   # app-only roles
uv run python examples/entraid/applications/grant_delegated_perms.py     # delegated scopes
```

Each prompts for the permission name, e.g. `Sites.FullControl.All` or `User.Read.All`.

### 4. User context (ROPC / delegated)

`OFFICE365_USERNAME` is the primary test user and the ROPC account; the optional
`OFFICE365_USERNAME_ALT` adds a second account for sharing/delegation tests.

```dotenv
OFFICE365_USERNAME=user1@contoso.onmicrosoft.com
OFFICE365_PASSWORD=your-password
# OFFICE365_USERNAME_ALT=user2@contoso.onmicrosoft.com
```

Needs MFA off for the ROPC user. For interactive examples, also add a redirect URI and
the **Allow public client flows** toggle:

```bash
uv run python examples/entraid/applications/redirect_uris.py
```

### 5. App-only

The guided wizard generates `.env` for you. It reads the values already present,
prompts only for the tenant and sign-in app id when they are missing, signs in,
reuses or generates one self-signed certificate (valid for both Graph and
SharePoint), optionally creates a client secret, and derives the SharePoint URLs
from the tenant name (or the signed-in UPN). Entra reveals a secret's value only
at creation, so the wizard asks whether to create one (default no) unless a secret
is already configured:

```bash
uv run python -m tests.setup
```

Everything else — the admin/primary usernames, the optional secondary user and
shared mailbox, and the `*_SITE_URL` defaults — is discovered or derived.
Re-running reuses what is already there; `--dry-run` previews the `.env` merge
without signing in or writing. The file holds an app secret and the admin account,
so it is written with mode `600` (and so is the `.env.bak` it leaves behind):

```bash
uv run python -m tests.setup --dry-run
```

Pass `--with-secret` to create one without prompting, or `--no-secret` to never
create one (`--yes` runs default to no). If `OFFICE365_CLIENT_SECRET` is left
empty, setup prints how to add it later.

Prerequisite: the app allows public client flows and has the delegated
`Application.ReadWrite.All` permission with admin consent (steps 2–3). Other
permissions are granted by `--grant` (step 3). Prefer the individual scripts?

```bash
# Certificate (Graph)
uv run python examples/entraid/applications/rotate_cert.py --generate

# SharePoint app-only, full cycle (cert + Sites.Selected + per-site access + .env)
uv run python examples/sharepoint/getting-started/setup_sharepoint_app.py \
    --site https://contoso.sharepoint.com/sites/project

# Client secret (Graph only — SharePoint REST API v1 rejects secrets)
uv run python examples/entraid/applications/rotate_secret.py
```

Then run tests and examples — missing credentials are skipped, not failed:

```bash
uv run pytest -q
uv run python examples/auth/with_client_secret.py
```

## Check what the live suites need

A live test states its precondition beside itself — `@requires_delegated("Mail.Read")`,
`@requires_application("Sites.Read.All")` — and skips when the tenant does not grant it.
The declared requirements are read off the test tree, so what a tenant must grant is
known before a run and never kept in a second list:

```bash
uv run python -m tests.preflight                      # the matrix, no credentials needed
uv run python -m tests.preflight --verify             # ... and what this tenant grants
uv run python -m tests.preflight --verify --report tests-report
```

`--report` writes `tests-report/preflight.md`: a table per suite (flow, tests, declared
permission, `met` / `missing …`). `--json tests-report` writes the same matrix as
`preflight.json` for a tool to read; nothing in the repo consumes it yet, so it is
opt-in rather than something every run pays for. Both files describe *a tenant*, not the
library, so `tests-report/` is gitignored. `--strict` exits non-zero when a flow is not
configured or a declared requirement is not met.

A skipped test run says the same thing in its summary — `2 tests skipped: application:
any of Domain.Read.All` — so a green-but-skipped run names what it did not exercise
rather than just counting.

### Grant what the suites need

`tests.preflight` answers "what is missing"; the setup wizard can close the gap, because
it is the one program that already signs in as an administrator:

```bash
uv run python -m tests.setup --grant --dry-run        # the plan, nothing granted
uv run python -m tests.setup --grant                  # asks, grants, re-reads the tenant
uv run python -m tests.setup --grant -y               # same, no prompt (CI / scripted)
```

The plan is the *smallest* set that would unblock the tree — one name per any-of group,
shared names asked for once — so the wizard does not request `Mail.ReadWrite` when
`Mail.Read` is enough. It prints the plan and waits for confirmation; `--dry-run` stops
there. Sign in with `--admin <upn>` (or `--interactive` for the browser flow) as an
account holding **Global Administrator** or **Privileged Role Administrator**: delegated
consent and application-role assignment are tenant-wide changes. Grants are idempotent —
an already-granted permission is skipped, a refused one is reported and the rest are
still attempted — and the wizard re-reads the tenant afterwards, so "done" means the
answer changed, not that the call returned.

Two kinds of requirement are reported but not granted, because they are not permissions
on your app: a **directory role** is assigned to the test user (and needs Entra ID P1/P2),
and a **license** has to be bought before it can be assigned. The plan names them and
says so.

Both the runtime check and the report go through `tests/capabilities.py`, which asks the
tenant one question per declared fact using the library's own
`office365.directory.permissions.guard` helpers. Nothing calls a test to learn what it
declares.

### Compared with other SDKs

Mature SDKs separate the two tiers the same way: `azure-sdk-for-python` records
fixtures and runs live only under `AZURE_TEST_RUN_LIVE`, listing each package's env
vars and role assignments in its `tests/README.md`; Terraform providers and Google
Cloud's `nox -s integration` gate live suites behind an opt-in environment variable;
AWS SDK integration suites live outside the default collection and fail with
`AccessDenied` at run time. The prerequisites in those projects are documented by hand,
next to the tests, and drift. Here they are declared by the test and read back, and
the answer is resolved through the same guard the library gives users — so a permission
gap is reported the way the library itself would report it.

## Publish a release

Publishing is a tag push; `.github/workflows/release.yml` builds and uploads the
wheels. The tag must match `project.version` in `pyproject.toml` — the workflow
refuses a mismatch:

```bash
git tag -a v3.3.0 -m "3.3.0"
git push origin v3.3.0
```

The GitHub release is then created by hand on the
[Releases page](https://github.com/vgrem/office365-rest-python-client/releases/new):
pick the `v3.3.0` tag, title it `v3.3.0`, and write the body from the matching
`CHANGELOG.md` section — a short summary, the `### ✨ Highlights`, the
`### ⚠️ Breaking changes` block, the fixes worth calling out, and the changelog +
install footer. `CHANGELOG.md` stays the exhaustive record; the release page is
the curated read.
