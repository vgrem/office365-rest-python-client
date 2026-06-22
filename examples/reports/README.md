# Microsoft Graph Reports

Examples for working with Microsoft Graph usage reports —
MFA status, email activity, mailbox storage, Teams/SharePoint/OneDrive
usage, and more.

---

## Prerequisites

| Permission | Description |
|---|---|
| `Reports.Read.All` | Download CSV usage reports |
| `AuditLog.Read.All` | Read MFA registration details |

---

## Examples

| Scenario | File | Permission |
|---|---|---|
| MFA registration status for all users | [`get_mfa_status.py`](./get_mfa_status.py) | `AuditLog.Read.All` |
| Download and parse CSV usage reports | [`usage_reports.py`](./usage_reports.py) | `Reports.Read.All` |

---

## Official docs

- [Microsoft Graph reports API overview](https://learn.microsoft.com/en-us/graph/api/resources/report)
- [MFA registration details API](https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails)
