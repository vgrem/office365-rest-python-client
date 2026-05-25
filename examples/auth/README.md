# Microsoft Graph Authentication

GraphClient supports the following authentication flows.

| Flow | Method | File | Notes |
|------|--------|------|-------|
| **Client secret** | `with_client_secret(client_id, secret)` | [`with_client_secret.py`](./with_client_secret.py) | App-only, simplest setup |
| **Certificate** | `GraphClient(tenant).with_client_certificate(client_id, thumbprint, key)` | [`with_client_cert.py`](./with_client_cert.py) | App-only, more secure |
| **Interactive** | `with_token_interactive(client_id)` | [`interactive.py`](./interactive.py) | User + MFA compatible |
| **ROPC** | `with_username_and_password(client_id, username, password)` | [`with_user_creds.py`](./with_user_creds.py) | User, no MFA |
| **National cloud** | `AzureEnvironment.USGovernmentHigh` | [`gcc_high.py`](./gcc_high.py) | GCC, DoD, China |

```python
from office365.graph_client import GraphClient

# Client secret (recommended for app-only)
client = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret(
    client_id="your_client_id", client_secret="your_secret"
)

# Interactive (MFA-compatible)
client = GraphClient(tenant="contoso.onmicrosoft.com").with_token_interactive(
    client_id="your_client_id"
)
```

---

## Official docs

- [Microsoft Graph authentication overview](https://learn.microsoft.com/en-us/graph/auth)
- [Microsoft identity platform auth flows](https://learn.microsoft.com/en-us/azure/active-directory/develop/msal-authentication-flows)
