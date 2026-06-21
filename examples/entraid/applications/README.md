# Application Registration & Permissions

Manage app registrations, certificate credentials, and API permissions.

## App Management

| What | File | Notes |
|------|------|-------|
| **List apps** | [`list.py`](./list.py) | First 100 app registrations |
| **Create app** | [`create.py`](./create.py) | Register a new app + cleanup |
| **Get by app ID** | [`get_by_app_id.py`](./get_by_app_id.py) | Find an app registration by its client ID |
| **Add certificate** | [`rotate_cert.py`](rotate_cert.py) | Upload a certificate to an app registration |
| **Add password** | [`rotate_password.py`](rotate_password.py) | Create a client secret for an app |
| **Rotate secret** | [`rotate_secret.py`](rotate_secret.py) | Generate a new client secret interactively |
| **Update redirect URIs** | [`redirect_uris.py`](./redirect_uris.py) | Add or update app redirect URIs |
| **Consolidated credentials report** | [`credentials_report.py`](./credentials_report.py) | All apps with passwords + certs + expiry |

## Permission Management

Check, list, grant, and revoke delegated or application permissions for an app.

### Check & List

| What | File | Notes |
|------|------|-------|
| **Check delegated perms** | [`has_delegated_perms.py`](./has_delegated_perms.py) | Does the app have a specific OAuth scope? |
| **Check application perms** | [`has_application_perms.py`](./has_application_perms.py) | Does the app have a specific app role? |
| **List delegated perms** | [`list_delegated_perms.py`](./list_delegated_perms.py) | All OAuth scopes granted to the app |
| **List application perms** | [`list_application_perms.py`](./list_application_perms.py) | All app roles granted to the app |
| **Find consent grants** | [`consent_graants.py`](./consent_graants.py) | Enumerate existing OAuth consent grants |

### Grant & Revoke

| What | File | Notes |
|------|------|-------|
| **Grant delegated perms** | [`grant_delegated_perms.py`](./grant_delegated_perms.py) | Grant an OAuth scope via admin consent (interactive) |
| **Grant application perms** | [`grant_application_perms.py`](./grant_application_perms.py) | Grant an app role (admin consent) |
| **Revoke delegated perms** | [`revoke_delegated_perms.py`](./revoke_delegated_perms.py) | Remove an OAuth scope grant |
| **Revoke application perms** | [`revoke_application_perms.py`](./revoke_application_perms.py) | Remove an app role assignment |

## Auditing & Compliance

| What | File | Notes |
|------|------|-------|
| **Password expiry** | [`password_expiry.py`](./password_expiry.py) | Find app passwords expiring within 30 days |
| **Certificate expiry** | [`certificate_expiry.py`](./certificate_expiry.py) | Find app certificates expiring within 30 days |
| **Find orphaned apps** | [`find_orphans.py`](./find_orphans.py) | Apps and service principals without owners |
| **Service principal credential audit** | [`sp_report.py`](./sp_report.py) | SP passwords and certs with expiry status |
| **List certificates** | [`list_certificates.py`](./list_certificates.py) | App certificates with validity status |
| **Grant Sites.Selected** | [`grant_site_selected_permission.py`](./grant_site_selected_permission.py) | Grant app access to a specific SharePoint site |

---

## Official docs

- [Register an application](https://learn.microsoft.com/en-us/graph/auth-register-app-v2)
- [Permissions grant via Graph API](https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph)
