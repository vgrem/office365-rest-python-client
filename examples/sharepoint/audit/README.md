# Audit Logs

Query audit logs from SharePoint sites and Microsoft Graph.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Site Owner** role | Required to read site-level audit settings. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |
| **AuditLog.Read.All** (Graph, delegated) | Required for sign-in logs and directory audits. | [Audit log permissions](https://learn.microsoft.com/en-us/graph/api/signin-list) |

---

## Examples

| Step | Operation | File | Required role / permission | API reference |
|---|---|---|---|---|
| **1** | Site audit — get audit configuration for a SharePoint site | [`site_audit.py`](./site_audit.py) | Site Owner | [SharePoint audit API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/audit) |
| **2** | Sign-in logs — query Azure AD sign-in logs | [`signin_logs.py`](./signin_logs.py) | `AuditLog.Read.All` | [Graph sign-in logs](https://learn.microsoft.com/en-us/graph/api/signin-list) |
| **3** | Directory audits — query Azure AD directory audit logs | [`directory_audits.py`](./directory_audits.py) | `AuditLog.Read.All` | [Graph directory audits](https://learn.microsoft.com/en-us/graph/api/directoryaudit-list) |
| **4** | File sharing audit events — detect when users share files | [`file_sharing_audit.py`](./file_sharing_audit.py) | `AuditLog.Read.All` | [Graph auditLogQuery](https://learn.microsoft.com/en-us/graph/api/security/auditlogquery-query) |

> For **unified audit log export** (Office 365 Management API), use the Microsoft Graph API directly.
> This library does not yet expose the unified audit log export endpoints.

---

## Quick start

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)

# Read site audit settings
audit = ctx.web.audit.get().execute_query()
print(f"Audit entries trimmed: {audit.audit_log_trimming_retention}")
```

---

## API reference

- [SharePoint audit REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/audit)
- [Graph sign-in logs API](https://learn.microsoft.com/en-us/graph/api/signin-list)
- [Graph directory audits API](https://learn.microsoft.com/en-us/graph/api/directoryaudit-list)