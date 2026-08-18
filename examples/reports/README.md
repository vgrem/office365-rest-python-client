# Microsoft Graph Reports

Examples for working with Microsoft Graph usage reports —
MFA status, email activity, mailbox storage, Teams/SharePoint/OneDrive
usage, M365 apps (incl. Copilot), and more.

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
| Generic CSV usage report download (argparse) | [`usage_reports.py`](./usage_reports.py) | `Reports.Read.All` |
| Teams user activity report | [`teams_usage.py`](./teams_usage.py) | `Reports.Read.All` |
| Microsoft 365 apps usage (incl. Copilot) | [`m365_apps_usage.py`](./m365_apps_usage.py) | `Reports.Read.All` |

### Copilot

| Scenario | File | Permission |
|---|---|---|
| Copilot license adoption | [`copilot/license_report.py`](./copilot/license_report.py) | `Organization.Read.All` |
| Copilot usage (M365 apps report) | [`copilot/usage_report.py`](./copilot/usage_report.py) | `Reports.Read.All` |
| Underused Copilot licenses | [`copilot/underused_licenses.py`](./copilot/underused_licenses.py) | `Organization.Read.All`, `User.Read.All` |

---

## Available reports (via `usage_reports.py --report`)

| Report | Graph method |
|---|---|
| Email activity counts | `get_email_activity_counts` |
| Mailbox usage storage | `get_mailbox_usage_storage` |
| OneDrive activity user counts | `get_onedrive_activity_user_counts` |
| SharePoint activity user counts | `get_sharepoint_activity_user_counts` |
| SharePoint site usage counts | `get_sharepoint_site_usage_site_counts` |
| Teams user activity counts | `get_teams_user_activity_user_counts` |
| Teams team counts | `get_teams_team_counts` |
| M365 apps user counts (incl. Copilot) | `get_m365_app_user_counts` |
| Office 365 activations user counts | `get_office365_activations_user_counts` |

---

## Official docs

- [Microsoft Graph reports API overview](https://learn.microsoft.com/en-us/graph/api/resources/report)
- [MFA registration details API](https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails)
