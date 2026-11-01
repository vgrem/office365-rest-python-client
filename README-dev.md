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

### From an IDE

An IDE's test runner is handed a path, not a command line, so a suite picked in the test
tree runs offline however many times you click it. Two ways out, both once per checkout:

- **Switch the checkout on** — put `OFFICE365_LIVE=1` in `.env`. `tests/settings.py` gives
  `.env` to the environment, so every runner in this checkout signs in: the test tree, a
  debugger, a bare `uv run pytest`. `--offline` still wins for the run that must not, and
  CI has no `.env`, so nothing there changes.
- **Or give the runner the flag** — VS Code: `"python.testing.pytestArgs": ["tests",
  "--live"]` in `.vscode/settings.json`; PyCharm: *Run → Edit Configurations → Edit
  configuration templates… → Python tests → pytest → Additional arguments*. A template
  covers every run created after it.

`python -m tests.doctor` ends its report with which of the two is in force.

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

Once `.env` exists, `tests.preflight` can grant everything the live suites declare and
the tenant lacks — it reads the requirement matrix, prints the plan, asks, grants, and
re-reads the tenant (see [Grant what the suites need](#grant-what-the-suites-need)):

```bash
uv run python -m tests.preflight --verify    # what is missing, without changing anything
uv run python -m tests.preflight --grant     # the same, then grant it
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

Two values a tenant reveals once and never returns again are the certificate thumbprint
and a client secret. Both come from the scripts that create them, not from a wizard:

```bash
uv run python examples/entraid/applications/rotate_cert.py     # prints OFFICE365_CERT_THUMBPRINT
uv run python examples/entraid/applications/rotate_secret.py   # prints CLIENT_SECRET, once
```

Those two lines, the URLs, usernames and mailboxes the comments in `.env.example` ask
for, and the app registration from step 2 are the whole file. Nothing writes it — it
holds an app secret and the admin account, and a program that can rewrite it can also
truncate it.

SharePoint has an end-to-end variant that provisions the app, attaches the certificate
the live suites read (`tests/selfsigncert.crt`), grants `Sites.Selected` plus one role
per site, and prints the same block:

```bash
uv run python examples/sharepoint/getting-started/setup_sharepoint_app.py --site <url>
```

A client secret signs in Graph but not the SharePoint REST API v1, which wants a
certificate — that is why both exist.

Then run tests and examples — missing credentials are skipped, not failed:

```bash
uv run pytest -q
uv run python examples/auth/with_client_secret.py
```

## Check what the live suites need

A live test states its precondition beside itself and skips when the tenant does not
grant it. Prefer the derived form, which reads the permission from the model method the
test exercises instead of restating it:

```python
@requires_call(Message.send, bypass_roles=["Exchange Administrator"])
@requires_delegated("Mail.Read")          # a scope, by name
@requires_application("Sites.Read.All")   # an app role, by name
```

Add `flow="application"` to `@requires_call` for an app-only suite. The declared
requirements are read off the test tree, so what a tenant must grant is known before a
run and never kept in a second list. A requirement names the API it is granted on, so a
SharePoint test and a Graph test never compare one API's grants against the other's:

```bash
uv run python -m tests.preflight                      # what is blocking the most tests
uv run python -m tests.preflight --verify             # ... and what this tenant grants
uv run python -m tests.preflight --all                # every requirement, not just the blockers
uv run python -m tests.preflight --verify --report tests-report
```

`--verify` signs in once per configured flow — including the certificate — and asks each
app about its own grants, so the answer is about the identity that will run the tests.

The default view is the screen, not the matrix: the counts, only the flows that are not
ready, and the unmet requirements deduplicated and ranked by the tests they unblock —
`35 tests  delegated: Sites.Read.All (+1)  (or an administrator role; via 35 declared calls)`.
The alternatives collapse to `(+1)` because a blocker line only has to say what to grant;
`--all` spells them all out, and requirements already met collapse to a count.

The trailing `via` is the row's provenance: `@requires_call` stamps the model methods a test
derived its requirement from, so the report says not just how many tests a grant unblocks but
which calls ask for it — a grant twelve tests need and a grant one endpoint brings are
different decisions. `--all` spells those calls instead of counting them, and a requirement
stated by hand with `@requires_delegated` names no call and shows none.

`--report` writes `tests-report/preflight.md`: the table per suite (flow, tests,
declared permission, `via` calls, `met` / `missing …`), which is what you want when the
question is about one suite rather than "what next". `--markdown` prints that table instead
of the summary. `--json tests-report` writes the same matrix as `preflight.json` for a tool
to read; nothing in the repo consumes it yet, so it is opt-in rather than something every run
pays for. Both files describe *a tenant*, not the library, so `tests-report/` is
gitignored. `--strict` exits non-zero when a flow is not configured or a declared
requirement is not met.

A skipped test run says the same thing in its summary — `2 tests skipped: application:
any of Domain.Read.All` — so a green-but-skipped run names what it did not exercise
rather than just counting.

### Grant what the suites need

`tests.preflight` answers "what is missing"; `--grant` closes the gap, because it is the
one program that already signs in as an administrator:

```bash
uv run python -m tests.preflight --verify            # the plan, nothing granted
uv run python -m tests.preflight --grant             # asks, grants, re-reads the tenant
uv run python -m tests.preflight --grant -y           # same, no prompt (scripted)
```

The plan is the *smallest* set that would unblock the tree — one name per any-of group,
shared names asked for once — so it does not request `Mail.ReadWrite` when `Mail.Read`
is enough. It prints the plan and waits for confirmation, then signs in by device code
as an account holding **Global Administrator** or **Privileged Role Administrator**:
delegated consent and application-role assignment are tenant-wide changes. Grants are
idempotent — an already-granted permission is skipped, a refused one is reported and the
rest are still attempted — and it re-reads the tenant afterwards, so "done" means the
answer changed, not that the call returned.

Two kinds of requirement are reported but not granted, because they are not permissions
on your app: a **directory role** is assigned to the test user (and needs Entra ID P1/P2),
and a **license** has to be bought before it can be assigned. The plan names them and
says so.

### Adding a model method

A method that queues a request (`add_query`, `execute_query`, `execute_batch`) says which
permission it needs, or `tests/unit/test_permission_declarations.py` fails: `PENDING` there
counts the undeclared builders per service package, and both directions are ratcheted — a
new undeclared builder raises the count, and so does a declaration that disappears. Declaring
is one line beside the request:

```python
@require_permission(
    delegated=("Mail.Read",),
    application=("Mail.Read",),
    resource=ResourceName.Graph,
)
def get(self) -> Message: ...
```

`resource` is the API the names are granted on, defaulting to Microsoft Graph; a model under
`office365/sharepoint` names `ResourceName.SharePoint`, because the same name is a different
grant on each API.

A SharePoint method says one word instead, because its eight names are a ladder — `AllSites.Read`,
`.Write`, `.Manage`, `.FullControl` and the app-only `Sites.*.All` beside them — where each rung
does what the ones below it do:

```python
from office365.sharepoint.permissions import SiteLevel, site_access


@site_access(SiteLevel.WRITE)
def add_item(self, creation_information: ListItemCreationInformation) -> ListItem: ...
```

Name the **weakest** rung that works: a read-only endpoint that claims `MANAGE` makes a live test
skip on a tenant that could have run it.

A name has to be one the API actually publishes, and that is checked offline against
`office365/permissions/snapshots/` — one generated module per API, holding the names its own
service principal offers. When a name is wrong, or an API ships a new permission you want to
use, re-read the API and commit what it writes:

```bash
uv run python scripts/gen_permission_catalog.py
```

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
