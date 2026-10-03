# Local development

How to set up the `office365-rest-python-client` repository to run tests and the
runnable examples on your machine — including authentication.

There are two tracks. Start with the **offline** track: it needs no Microsoft 365
tenant and validates most code changes. Only switch on the **live** track when you
want to run integration tests or examples against a real tenant.

---

## TL;DR

```bash
git clone https://github.com/vgrem/office365-rest-python-client.git
cd office365-rest-python-client

uv venv
source .venv/bin/activate       # Windows: .venv\Scripts\activate
uv sync --all-extras

# 1) No tenant needed — run this first:
uv run pytest --offline -q

# 2) Optional: run live integration tests and examples against a tenant:
cp .env.example .env            # fill in the blocks you need (see below)
uv run python -m tests.doctor   # shows what is configured / what is missing
uv run pytest tests/sharepoint
uv run python examples/auth/with_client_secret.py
```

`.env` is `.gitignore`d and loaded automatically — you never `export` anything.

---

## Repository map

| Path | What it is |
|---|---|
| `office365/` | The library itself (generated + handwritten code). |
| `tests/unit/` | Offline unit tests. **No credentials, always run.** |
| `tests/**` (rest) | End-to-end tests against a real tenant. Skipped when unconfigured. |
| `tests/settings.py` | Central credential loader shared by tests **and** examples. |
| `tests/doctor.py` | Credential doctor: `python -m tests.doctor`. |
| `examples/` | Runnable scripts, one per service/scenario. Reuse the same `.env`. |
| `generator/` | Code-generation tooling for the service models. |
| `docs/` | MkDocs site sources. |

---

## Prerequisites

- **Python >= 3.8**
- [**uv**](https://docs.astral.sh/uv/) (recommended) or `pip`
- *For the live track only:* a Microsoft 365 tenant and permission to register an app.

### Install with uv (recommended)

```bash
uv venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
uv sync --all-extras
```

### Install with pip

```bash
python3 -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate
pip install -e ".[examples,ntlm]" pytest
```

---

## Configure authentication

All tests and examples read credentials from a single `.env` file in the project
root, via `tests/settings.py`. Copy the template and fill in only the blocks you
need — you do **not** need everything:

```bash
cp .env.example .env
```

### Which variables do I need?

Pick the row that matches what you want to run:

| I want to run | Flow | Variables to fill in `.env` | Also required |
|---|---|---|---|
| `tests/unit` | none | — | — |
| Graph **delegated** tests | `delegated-ropc` | `OFFICE365_TENANT`, `OFFICE365_CLIENT_ID`, `OFFICE365_USERNAME`, `OFFICE365_PASSWORD` | MFA disabled for the test user |
| Graph **app-only** tests | `app-only` | `OFFICE365_TENANT`, `OFFICE365_CLIENT_ID`, `OFFICE365_CLIENT_SECRET` | application permissions + admin consent |
| SharePoint tests & examples | `app-only-cert` | `OFFICE365_TENANT`, `OFFICE365_CLIENT_ID`, `OFFICE365_CERT_THUMBPRINT` | `tests/selfsigncert.pem` |
| Interactive / device-code / custom-token examples | `delegated` | `OFFICE365_TENANT`, `OFFICE365_CLIENT_ID` | redirect URI / app registration |

The flow names follow Microsoft's vocabulary — [delegated vs. app-only access](https://learn.microsoft.com/graph/auth/auth-concepts)
and SharePoint's [Entra ID App-Only](https://learn.microsoft.com/sharepoint/dev/solution-guidance/security-apponly-azuread) —
and are defined once in `tests/settings.py`.

### Check what is configured

```bash
uv run python -m tests.doctor
```

```
Auth readiness (environment + .env):
  Delegated access (interactive / device code / custom)  not ready  missing: OFFICE365_TENANT, OFFICE365_CLIENT_ID
  Delegated access (ROPC username + password)            not ready  missing: OFFICE365_TENANT, OFFICE365_CLIENT_ID, OFFICE365_USERNAME, OFFICE365_PASSWORD
  App-only access (client secret)                        not ready  missing: OFFICE365_TENANT, OFFICE365_CLIENT_ID, OFFICE365_CLIENT_SECRET
  App-only access (certificate / Entra ID App-Only)      not ready  missing: OFFICE365_TENANT, OFFICE365_CLIENT_ID, OFFICE365_CERT_THUMBPRINT, tests/selfsigncert.pem

  Tip: cp .env.example .env, fill it in, then re-run `python -m tests.doctor`.
```

To make a script or CI job fail fast, require a specific flow:

```bash
uv run python -m tests.doctor --require app-only-cert   # exits non-zero when not ready
```

### SharePoint app-only uses a certificate (Entra ID App-Only)

The SharePoint REST API (`/_api`) does not accept a client secret for app-only
access — it needs a certificate. Generate one and register it with your app in a
single step:

```bash
uv run python examples/sharepoint/auth/setup/certificate_auth.py \
    --site https://contoso.sharepoint.com/sites/project
```

The script creates `tests/selfsigncert.crt` / `tests/selfsigncert.pem`, uploads the
public key to your app registration, grants site access, and prints the
`Thumbprint`. Paste that value into `.env`:

```dotenv
OFFICE365_CERT_THUMBPRINT=6B36FBFC86FB1C019EB6496494B9195E6D179DDB
```

`tests/selfsigncert.pem` is the default `OFFICE365_CERT_PATH`; point it
elsewhere if your certificate lives elsewhere. See
[`examples/sharepoint/auth/`](examples/sharepoint/auth/) for the full picture
(client secret works on **Graph**, certificate is required for **SharePoint**).

---

## Running tests

```bash
# Offline unit tests — no tenant, always run (this is what CI runs):
uv run pytest --offline -q

# Everything (offline tests run; live tests run if their credentials are set):
uv run pytest -q

# A single area or file:
uv run pytest tests/sharepoint
uv run pytest tests/directory/test_user.py
```

Live tests that need credentials you have not configured are **skipped with a
reason**, not failed. At the end of a run pytest prints what was skipped and why:

```
======================= auth credentials not configured ========================
Delegated access (ROPC username + password): missing OFFICE365_CLIENT_ID, OFFICE365_USERNAME, OFFICE365_PASSWORD
Copy .env.example to .env and fill it in, then run `python -m tests.doctor`.
Pass --offline to make this quiet.
```

`--offline` skips **all** live integration tests explicitly (useful in CI and on a
machine without credentials).

---

## Running examples

Every script under `examples/` is runnable and reuses the same `.env`:

```bash
uv run python examples/auth/with_client_secret.py
uv run python examples/sharepoint/lists/list_items.py
uv run python examples/outlook/send_email.py
```

If a script's credentials are missing it stops immediately with an actionable
message (for example: `The 'app-only' credentials are not configured. Missing:
OFFICE365_CLIENT_SECRET ...`). Run `python -m tests.doctor` to see the full
picture before running anything.

---

## Required tenant roles

For the full end-to-end suite, assign these
[Microsoft Entra roles](https://learn.microsoft.com/en-us/azure/active-directory/roles/permissions-reference)
to the test account:

- Global reader
- Groups admin
- Search admin
- SharePoint admin
- Teams service admin
- Users admin

Some tests additionally require specific Graph **application permissions** with
admin consent (for example `Sites.FullControl.All`, `Mail.Read`, `User.Read.All`).

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `Credentials are not configured ...` | You ran a live test/example without a complete `.env`. Run `python -m tests.doctor`, then fill in the missing values (or use `--offline`). |
| Lots of `s` (skipped) and no live tests | Expected without credentials — see the "auth credentials not configured" summary. |
| SharePoint HTTP 401 / `invalid_client` | Certificate thumbprint does not match, or `tests/selfsigncert.pem` is missing. Re-run `certificate_auth.py` and update `OFFICE365_CERT_THUMBPRINT`. |
| Graph HTTP 403 | The app is missing an application permission or admin consent. |
| ROPC login fails | Security defaults / MFA block the password grant for that user. |

---

## Code style & related docs

```bash
uv run ruff check --fix .
uv run ruff format .
uv run pyright
```

- [CONTRIBUTING.md](CONTRIBUTING.md) — contribution workflow and PR process
- [examples/README.md](examples/README.md) — the full example catalog
- [README.md](README.md) — library overview and usage
