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
uv run python -m tests.preflight                      # what is blocking the most tests
uv run python -m tests.preflight --verify             # ... and what this tenant grants
uv run python -m tests.preflight --all                # every requirement, not just the blockers
uv run python -m tests.preflight --verify --report tests-report
```

The default view is the screen, not the matrix: the counts, only the flows that are not
ready, and the unmet requirements deduplicated and ranked by the tests they unblock —
`35 tests  delegated: Sites.Read.All (+1) or an administrator role`. The alternatives
collapse to `(+1)` because a blocker line only has to say what to grant; `--all` spells
them all out, and requirements already met collapse to a count.

`--report` writes `tests-report/preflight.md`: the table per suite (flow, tests,
declared permission, `met` / `missing …`), which is what you want when the question is
about one suite rather than "what next". `--markdown` prints that table instead of the
summary. `--json tests-report` writes the same matrix as `preflight.json` for a tool to
read; nothing in the repo consumes it yet, so it is opt-in rather than something every
run pays for. Both files describe *a tenant*, not the library, so `tests-report/` is
gitignored. `--strict` exits non-zero when a flow is not configured or a declared
requirement is not met.

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

A model method carries the same kind of statement. `@require_permission(delegated=...,
application=...)` marks 184 request builders in 52 modules, and both sides now produce
the one `Requirement` type: `PermissionRequirement.requirements()` turns a method's
declaration into one requirement per flow it can run under, with `directory_roles`
becoming the bypass a test spells as `bypass_roles`. Nothing calls a method to learn what
it declares either — the stamp is `method.__required_permissions__`, and
`office365.permissions.declared(method, flow=...)` reads it, raising rather than returning
an empty requirement when the method names nothing under the flow asked for.

All of it lives in one package, three modules, so the vocabulary is the API:
`office365.permissions.declaration` (the marker and `declared()`),
`office365.permissions.requirement` (`Requirement`, `Requirement.join`, the flow list) and
`office365.permissions.index` (the whole-package walk). A live test imports
`Requirement` and `declared` from `office365.permissions`; nothing under `tests/` owns a
copy of the rules.

A declaration names the **API resource** the names belong to, and the fourth module
`office365.permissions.resource` is that vocabulary (`ResourceName.Graph`,
`ResourceName.SharePoint`, `ResourceName.Exchange`, ...). The resource is not decoration:
`Sites.ReadWrite.All` is granted on Microsoft Graph *and* on SharePoint, `Mail.Send` is an
application permission on Graph but a delegated one on Exchange Online, and a name is only a
grant on the API that defines it. So `@require_permission(resource=ResourceName.SharePoint,
...)` is how a model under `office365/sharepoint` says which grants it needs, `Requirement`
carries the resource into the check, and `Requirement.join` refuses to merge two APIs' names
into one group — the group would compare names that mean different things. The default is
Microsoft Graph, which is what all 184 declarations written so far mean, so adding the
dimension changed no rendered requirement: preflight output is byte-identical.

That is step 1 of `design/0002-declared-permissions.md`: a permission matrix assembled
from declarations instead of typed, which preflight can join with the test declarations so
a scope is priced by the endpoints it unlocks as well as by the tests it unblocks.

The declarations are ratcheted per service package, not banned: `PENDING` in
`tests/unit/test_permission_declarations.py` records how many public operations still name
no permission, and the map only shrinks. Both directions fail — a new undeclared request
builder raises a count, and a declaration that disappears raises one too. Outlook is absent
from the map because it is closed: 21 request builders, every one declared, which makes it
the pilot for reading markers instead of re-stating them in a test. What stays out of scope
is stated in the test: `runtime` and `migration` orchestrate requests that model methods
already declare, and the root-level base classes cannot know the type they create.

What the ratchet asks — which methods queue a request, and which of them name nothing — is
answered by the library, not by the test: `office365.permissions.index(office365)` returns an
`Index` whose `declared()`, `undeclared()` and `debt()` answer over one walk of the tree, so
the ledger is a number and not a rumour. Before this, three consumers each parsed the source:
the ratchet with `ast`, and any tool that wanted a type's scopes with a walker of its own.
The index reads bytecode names instead, so an annotation such as `-> EdiscoveryReviewSetQuery`
is no longer mistaken for an operation, and it does not use `pkgutil.walk_packages` — that walk
skips a directory without an `__init__.py`, which is every namespace-package subtree in this
library, so a ledger built on it would under-report.

Nothing registers itself. An earlier version had `ClientObject.__init_subclass__` and the
decorator push into two module-level registries that `runtime` then had to keep in sync; the
index instead imports the tree once and reads it, so `runtime` does not depend on the
permissions package, an answer cannot depend on what a process happened to import first, and
`index()` is a memoized pure function of the package.

Discovery is one rule, deliberately: a method that submits a query (`add_query`,
`execute_query`, `execute_batch`) issues a request. An earlier version also counted anything
whose name ended in `Query`, which found 16 more builders but also `ImageInfo.__eq__`,
`BatchQuery.get_queries` and `AuditLogQuery` — a name suffix is a guess, and one rule that
nobody has to interpret is worth a floor that is 16 methods lower. The count is therefore a
floor in two senses: a method that delegates its request to a declared sibling is invisible
(`Entity.get` queues nothing), and a method that only builds a query and returns it is not
counted. Both directions of the ratchet still bite, because a *new* undeclared builder is
caught by the same rule that the map was measured with.

A live test can read that declaration instead of restating it: `@requires_call(Message.send,
bypass_roles=[...])` joins the declared requirements of every method the test exercises and
stamps one `Requirement`, so the skip, the preflight row and the model's own answer cannot
drift apart. The join itself is `Requirement.join(*declarations, flow=...)` in the library: a
test, a migration job and a user's script ask the same question and get the same answer, and a
call that names nothing under the requested flow raises instead of producing an empty
requirement that would always pass. `tests/outlook/test_outlook_user.py` is the first suite converted — five of its
seven tests now name no scope — and converting it removed two over-declarations rather than
adding any: a test claimed four `User.*` alternatives where the model declares `User.Read`,
and `Mail.Read.Shared` where the call declares `Mail.Read`/`Mail.ReadWrite`. The two tests
that still restate their scopes say why in a comment: they call the generic `Entity.get`,
which declares nothing because it cannot know the type it reads.

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
