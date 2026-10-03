# Connect to SharePoint Online with certificate credentials

SharePoint app-only automation authenticates with an **X.509 certificate** — the
SharePoint REST endpoints (`/_api`) do not accept a **client secret**. This folder
contains an automated setup script plus the manual steps.

## Automated setup (recommended)

```bash
uv run python examples/sharepoint/auth/setup/certificate_auth.py \
    --site https://contoso.sharepoint.com/sites/project
```

The script:

1. generates `tests/selfsigncert.crt` and `tests/selfsigncert.pem`,
2. uploads the public certificate to your app registration,
3. grants the app access to the target site (`Sites.Selected`),
4. prints the values to put in `.env`, including the certificate **thumbprint**.

```dotenv
OFFICE365_TENANT=contoso.onmicrosoft.com
OFFICE365_CLIENT_ID=51d03106-4726-442c-86db-70b32fa7547f
OFFICE365_CERT_THUMBPRINT=6B36FBFC86FB1C019EB6496494B9195E6D179DDB
```

It authenticates as a tenant administrator (`OFFICE365_ADMIN_USERNAME`) via
interactive sign-in and requires the **Global Administrator** or **Privileged Role
Administrator** role. See
[README-dev.md](https://github.com/vgrem/office365-rest-python-client/blob/master/README-dev.md)
for the full local setup.

## Manual setup

1. **Create a self-signed certificate** (Azure Cloud Shell or locally):

   ```bash
   openssl req -x509 -sha256 -nodes -days 365 -newkey rsa:2048 \
       -keyout privateKey.key -out selfsigncert.crt
   cat selfsigncert.crt privateKey.key > selfsigncert.pem
   ```

2. **Register the certificate** with your app in Entra ID — see the
   [official steps](https://learn.microsoft.com/en-us/entra/identity-platform/howto-create-self-signed-certificate).

3. **Grant SharePoint permissions**: *Add a permission* → *Microsoft APIs* →
   **SharePoint** → **Application permissions** → e.g. `Sites.FullControl.All`
   (or `Sites.Selected` for per-site access).

4. **Note the thumbprint** (hex, no colons) and point `OFFICE365_CERT_THUMBPRINT`
   at it.

## Use in code

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_certificate(
    tenant="contoso.onmicrosoft.com",
    client_id="51d03106-4726-442c-86db-70b32fa7547f",
    thumbprint="6B36FBFC86FB1C019EB6496494B9195E6D179DDB",
    cert_path="tests/selfsigncert.pem",
)

web = ctx.web.get().execute_query()
print(web.url)
```

For other variants (private key as a string, custom scopes) and the user-context
flows, see [the modern authentication examples](../modern/).

## References

- [Grant app-only access to SharePoint Online](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread)
- [How to create a self-signed certificate with Azure Cloud Shell](https://techcommunity.microsoft.com/t5/itops-talk-blog/how-to-create-a-self-signed-certificate-in-azure-using-cloud/ba-p/401403)
- [Create a self-signed certificate via PowerShell](https://learn.microsoft.com/en-us/powershell/module/pkiclient/new-selfsignedcertificate)
