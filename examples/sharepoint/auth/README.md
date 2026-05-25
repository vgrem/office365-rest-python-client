# SharePoint Authentication

ClientContext supports the following authentication flows.

## Modern (Azure AD)

| Flow | Method | File | Notes |
|------|--------|------|-------|
| **Certificate** | `with_client_certificate(tenant, client_id, thumbprint, cert_path)` | [`modern/with_certificate.py`](./modern/with_certificate.py) | App-only, recommended |
| **Username & password** | `with_username_and_password(tenant, client_id, user, pass)` | [`modern/with_username_and_password.py`](./modern/with_username_and_password.py) | User (MSAL ROPC), no MFA |
| **Interactive** | `with_interactive(tenant, client_id)` | [`modern/with_interactive.py`](./modern/with_interactive.py) | User + MFA |
| **Device code** | `with_device_flow(tenant, client_id)` | [`modern/with_device_flow.py`](./modern/with_device_flow.py) | User + MFA, headless |
| **Cookies** | `with_cookies(...)` | [`modern/with_cookies.py`](./modern/with_cookies.py) | Browser session reuse |
| **Capture cookies** | Playwright | [`capture_cookies_with_playwright.py`](./capture_cookies_with_playwright.py) | Automated cookie capture |

## Legacy (deprecated / on-prem)

| Flow | File | Status |
|------|------|--------|
| **ACS app-only** | [`legacy/with_app_only.py`](./legacy/with_app_only.py) | 🚫 Retired Apr 2026 (on-prem only) |
| **SAML user auth** | [`legacy/with_user_credential.py`](./legacy/with_user_credential.py) | 🚫 Retired May 2026 |
| **NTLM** (on-prem) | [`legacy/with_ntlm.py`](./legacy/with_ntlm.py) | ✅ On-prem only |

```python
from office365.sharepoint.client_context import ClientContext

# Certificate (recommended for app-only automation)
ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_certificate(
    tenant="contoso.onmicrosoft.com",
    client_id="your_client_id",
    thumbprint="your_thumbprint",
    cert_path="./cert.pem",
)

# Username & password (MSAL ROPC)
ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_username_and_password(
    tenant="contoso.onmicrosoft.com",
    client_id="your_client_id",
    username="user@contoso.com",
    password="your_password",
)
```

---

## Official docs

- [SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api)
- [Security app-only Azure AD](https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azuread)
