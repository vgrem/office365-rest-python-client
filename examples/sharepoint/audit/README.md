# Audit Logs

Query audit logs from SharePoint sites and Microsoft Graph.

| What | File | Notes |
|------|------|-------|
| **Site audit settings** | [`site_audit.py`](./site_audit.py) | Get audit configuration for a SharePoint site |
| **Sign-in logs** (Graph) | [`signin_logs.py`](./signin_logs.py) | Azure AD sign-in logs (requires `AuditLog.Read.All`) |
| **Directory audits** (Graph) | [`directory_audits.py`](./directory_audits.py) | Azure AD directory audit logs |

> For **unified audit log export** (Office 365 Management API), use the Microsoft Graph API directly.
> This library does not yet expose the unified audit log export endpoints.

---

## Official docs

- [SharePoint audit REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/audit)
- [Graph sign-in logs API](https://learn.microsoft.com/en-us/graph/api/signin-list)
- [Graph directory audits API](https://learn.microsoft.com/en-us/graph/api/directoryaudit-list)
