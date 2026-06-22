# Application Registration & Permissions

Manage app registrations, certificate credentials, and API permissions.

## App Management

| What | File | Notes |
|------|------|-------|
| **List apps** | [`list.py`](./list.py) | First 100 app registrations |
| **Create app** | [`create.py`](./create.py) | Register a new app + cleanup |
| **Get by app ID** | [`get_by_app_id.py`](./get_by_app_id.py) | Find an app registration by its client ID |
| **Add certificate** | [`rotate_cert.py`](rotate_cert.py) | Upload a certificate to an app |
| **Add password** | [`rotate_secret.py`](rotate_secret.py) | Create a client secret |
| **Update redirect URIs** | [`redirect_uris.py`](./redirect_uris.py) | Add or update app redirect URIs |
| **Consolidated credentials report** | [`credentials_report.py`](./credentials_report.py) | All apps with passwords + certs + expiry |

## Credential Renewal

| What | File | Notes |
|------|------|-------|
| **Renew secret if expiring** | [`renew_secret.py`](./renew_secret.py) | Check → if expiring in 30d, add replacement |
| **Renew cert if expiring** | [`renew_cert.py`](./renew_cert.py) | Check → if expiring in 30d, upload replacement |
| **Rotate all expired** | [`rotate_all_expired.py`](./rotate_all_expired.py) | Scan all apps → rotate every expired secret |
| **Clean up old credentials** | [`cleanup_old.py`](./cleanup_old.py) | Remove expired passwords past grace period |

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
| **Find stale apps** | [`find_stale_apps.py`](./find_stale_apps.py) | Apps where all credentials have expired |
| **Find orphaned apps** | [`find_orphans.py`](./find_orphans.py) | Apps and service principals without owners |
| **Service principal credential audit** | [`sp_report.py`](./sp_report.py) | SP passwords and certs with expiry status |
| **List certificates** | [`list_certificates.py`](./list_certificates.py) | App certificates with validity status |

## Cleanup & Remediation

| What | File | Notes |
|------|------|-------|
| **Remove expired passwords** | [`cleanup_old.py`](./cleanup_old.py) | Remove expired secrets from all apps |
| **Delete stale apps** | [`cleanup_stale.py`](./cleanup_stale.py) | Delete apps with no valid credentials |
| **Grant Sites.Selected** | [`grant_site_selected_permission.py`](./grant_site_selected_permission.py) | Grant app access to a specific SharePoint site |

---

## Official docs

- [Register an application](https://learn.microsoft.com/en-us/graph/auth-register-app-v2)
- [Permissions grant via Graph API](https://learn.microsoft.com/en-us/graph/permissions-grant-via-msgraph)
