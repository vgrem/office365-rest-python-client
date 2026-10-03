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
uv run pytest --offline -q
```

That is the whole setup for most contributions. Continue only to run against a real tenant.

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

Both scripts sign in as `OFFICE365_ADMIN_USERNAME` and apply admin consent:

```bash
uv run python examples/entraid/applications/grant_application_perms.py   # app-only roles
uv run python examples/entraid/applications/grant_delegated_perms.py     # delegated scopes
```

Each prompts for the permission name, e.g. `Sites.FullControl.All` or `User.Read.All`.

### 4. User context (ROPC / delegated)

```dotenv
OFFICE365_USERNAME=admin@contoso.onmicrosoft.com
OFFICE365_PASSWORD=your-password
```

Needs MFA off for that user. For interactive examples, also add a redirect URI and
the **Allow public client flows** toggle:

```bash
uv run python examples/entraid/applications/redirect_uris.py
```

### 5. App-only

**a. Certificate (SharePoint)** — SharePoint `/_api` requires a certificate, not a
secret. Generate it, upload it and grant site access in one command:

```bash
uv run python examples/sharepoint/auth/setup/certificate_auth.py \
    --site https://contoso.sharepoint.com/sites/project
```

It prints the value to paste:

```dotenv
OFFICE365_CERT_THUMBPRINT=<thumbprint>
```

**b. Client secret (Graph)** — create one, then grant app permissions (step 3):

```bash
uv run python examples/entraid/applications/rotate_secret.py
```

```dotenv
OFFICE365_CLIENT_SECRET=<secret>
```

Then run tests and examples — missing credentials are skipped, not failed:

```bash
uv run pytest -q
uv run python examples/auth/with_client_secret.py
```
