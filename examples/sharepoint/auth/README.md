# SharePoint Authentication

`ClientContext` supports multiple authentication flows. Choose based on your
scenario and environment.

---

## Auth decision flow

```mermaid
flowchart TD
    Start{"Target environment?"}
    Start -->|"SharePoint Online"| SPO
    Start -->|"SharePoint Server (on-prem)"| OnPrem

    SPO -->|"App-only (automation)"| Cert["MSAL Certificate\nrecommended"]
    SPO -->|"User context"| UserFlow
    UserFlow -->|"MFA supported"| Interactive["MSAL Interactive"]
    UserFlow -->|"No MFA"| ROPC["MSAL Username+Password"]

    OnPrem --> NTLM["NTLM"]
    OnPrem --> LegacyACS["ACS App-Only\n(if configured)"]
```

---

## Modern (Azure AD, recommended for SharePoint Online)

| Flow | Method | File | Notes |
|---|---|---|---|
| **Certificate (PEM file)** | `with_client_certificate(tenant, client_id, thumbprint, cert_path)` | [`modern/with_certificate.py`](./modern/with_certificate.py) | App-only, recommended for automation |
| **Certificate (private key)** | `with_client_certificate(..., private_key=...)` | [`modern/with_certificate_and_privkey.py`](./modern/with_certificate_and_privkey.py) | App-only, key passed as a string |
| **Certificate (custom scopes)** | `with_client_certificate(..., scopes=...)` | [`modern/with_certificate_and_scopes.py`](./modern/with_certificate_and_scopes.py) | App-only with explicit permission scopes |
| **Username & password** | `with_username_and_password(tenant, client_id, user, pass)` | [`modern/with_username_and_password.py`](./modern/with_username_and_password.py) | MSAL ROPC flow, **no MFA** |
| **Interactive** | `with_interactive(tenant, client_id)` | [`modern/with_interactive.py`](./modern/with_interactive.py) | User context with MFA support |
| **Device code** | `with_device_flow(tenant, client_id)` | [`modern/with_device_flow.py`](./modern/with_device_flow.py) | Headless / CLI with MFA |
| **Cookies** | `with_cookies(...)` | [`modern/with_cookies.py`](./modern/with_cookies.py) | Reuse browser session |
| **Capture cookies** | Playwright script | [`capture_cookies_with_playwright.py`](./capture_cookies_with_playwright.py) | Automated cookie capture |
| **Load cookies** | Playwright storage state | [`load_cookies_from_playwright.py`](./load_cookies_from_playwright.py) | Import ``storage_state.json`` from Playwright |

### Why a client secret doesn't work for SharePoint app-only

`ClientContext` talks to the SharePoint **REST** endpoints (`/_api`), and Microsoft's
app-only access to SharePoint Online requires **certificate** credentials. A
**client secret** is accepted by **Microsoft Graph**, but not by SharePoint's
`/_api` app-only flow — so `with_client_secret(...)` / `with_client_credentials(...)`
fail with `ClientContext`. Use `with_client_certificate(...)` (any variant above)
for app-only automation.

For app-only that *must* use a client secret (e.g. a Graph workflow), use
`GraphClient` (Microsoft Graph) instead — it supports `with_client_secret(...)`.

## Legacy, retired for SharePoint Online (on-prem only)

> **Important:** These flows have been **retired** for SharePoint Online.
> They remain available for **SharePoint Server (on-prem)** environments.
>
> - **ACS App-Only**, [Retired April 2, 2026](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/add-ins-and-azure-acs-retirements-faq)
> - **SAML / WS-Trust (SharePointOnlineCredentials)**, [Deprecated for SPO](https://learn.microsoft.com/en-us/answers/questions/5629577/basic-authentication-for-sharepoint-online-is-depr)

| Flow | File | Status | Scope |
|---|---|---|---|
| **ACS app-only** | [`legacy/with_app_only.py`](./legacy/with_app_only.py) | 🚫 Retired Apr 2026 | On-prem only |
| **SAML user auth** | [`legacy/with_user_credential.py`](./legacy/with_user_credential.py) | 🚫 Retired May 2026 | On-prem only |
| **NTLM** | [`legacy/with_ntlm.py`](./legacy/with_ntlm.py) | ✅ Current | On-prem only |

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

# — App-only automation (recommended) —
ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_certificate(
    tenant="contoso.onmicrosoft.com",
    client_id="your_client_id",
    thumbprint="your_thumbprint",
    cert_path="./cert.pem",
)

# — Interactive (user + MFA) —
ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_interactive(
    tenant="contoso.onmicrosoft.com",
    client_id="your_client_id",
)
```

---

## Official docs

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
- [Security app-only Azure AD](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread)
- [ACS retirement FAQ](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/add-ins-and-azure-acs-retirements-faq)
- [Basic authentication deprecation](https://learn.microsoft.com/en-us/answers/questions/5629577/basic-authentication-for-sharepoint-online-is-depr)
