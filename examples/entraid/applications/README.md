# Application Registration & Permissions

Manage app registrations, certificate credentials, and API permissions.

## App Management

| What | File | Notes |
|------|------|-------|
| **Add certificate** | [`add_cert.py`](rotate_cert.py) | Upload a certificate to an app registration |
| **Add password** | [`app_password.py`](rotate_password.py) | Create a client secret for an app |
| **Get by app ID** | [`get_by_app_id.py`](./get_by_app_id.py) | Find an app registration by its client ID |

## Permission Management

Check, list, grant, and revoke delegated or application permissions for an app.

### 🔍 Check & List

| What | File | Notes |
|------|------|-------|
| **Check delegated perms** | [`has_delegated_perms.py`](./has_delegated_perms.py) | Does the app have a specific OAuth scope? |
| **Check application perms** | [`has_application_perms.py`](./has_application_perms.py) | Does the app have a specific app role? |
| **List delegated perms** | [`list_delegated_perms.py`](./list_delegated_perms.py) | All OAuth scopes granted to the app |
| **List application perms** | [`list_application_perms.py`](./list_application_perms.py) | All app roles granted to the app |
| **Find consent grants** | [`find_consent_grants.py`](./find_consent_grants.py) | Enumerate existing consent grants + app role assignments |

### ✏️ Grant & Revoke

| What | File | Notes |
|------|------|-------|
| **Grant delegated perms** | [`grant_delegated_perms.py`](./grant_delegated_perms.py) | Grant an OAuth scope via admin consent (interactive) |
| **Grant application perms** | [`grant_application_perms.py`](./grant_application_perms.py) | Grant an app role (admin consent) |
| **Revoke delegated perms** | [`revoke_delegated_perms.py`](./revoke_delegated_perms.py) | Remove an OAuth scope grant |
| **Revoke application perms** | [`revoke_application_perms.py`](./revoke_application_perms.py) | Remove an app role assignment |

---

## Official docs

- [Register an application](https://learn.microsoft.com/en-us/graph/auth-register-app-v2)
- [Permissions grant via Graph API](https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph)
