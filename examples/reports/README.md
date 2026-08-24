# Microsoft Graph Reports

Usage and adoption reports across the main Microsoft 365 workloads — email
(Exchange), mailbox storage, OneDrive, SharePoint, Teams, Microsoft 365 apps
(including Copilot), Office activations, and MFA registration coverage.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Reports.Read.All` | Download CSV usage reports | [Reports permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#reports-permissions) |
| `AuditLog.Read.All` | MFA registration details | [Audit permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#auditlog-permissions) |
| `Organization.Read.All` | Subscribed SKUs (license reports) | [Organization permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#organization-permissions) |

All examples authenticate with client secret (`client_id`, `client_secret`,
`tenant` from `tests.settings`).

---

## Examples by workload

### Security — MFA coverage

| Operation | File | Permission | API |
|---|---|---|---|
| MFA registration status per user | [`get_mfa_status.py`](./get_mfa_status.py) | `AuditLog.Read.All` | [user registration details](https://learn.microsoft.com/en-us/graph/api/authenticationmethods-list-userregistrationdetails) |

### Exchange Online — email & mailbox

| Operation | File | API |
|---|---|---|
| Email activity counts (sent/read/received) | [`email_activity.py`](./email_activity.py) | [getEmailActivityCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getemailactivitycounts) |
| Mailbox storage usage trend | [`mailbox_storage.py`](./mailbox_storage.py) | [getMailboxUsageStorage](https://learn.microsoft.com/en-us/graph/api/reportroot-getmailboxusagestorage) |

### Files — OneDrive & SharePoint

| Operation | File | API |
|---|---|---|
| OneDrive activity (users, files, sharing) | [`onedrive_usage.py`](./onedrive_usage.py) | [getOneDriveActivityUserCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getonedriveactivityusercounts) |
| SharePoint site usage / storage | [`sharepoint_usage.py`](./sharepoint_usage.py) | [getSharePointSiteUsageSiteCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getsharepointsiteusagesitecounts) |

### Collaboration — Teams & apps

| Operation | File | API |
|---|---|---|
| Teams user activity | [`teams_usage.py`](./teams_usage.py) | [getTeamsUserActivityUserCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getteamsuseractivityusercounts) |
| Microsoft 365 apps usage (incl. Copilot) | [`m365_apps_usage.py`](./m365_apps_usage.py) | [getM365AppUserCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getm365appusercounts) |
| Office 365 activations per product | [`activations.py`](./activations.py) | [getOffice365ActivationCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getoffice365activationcounts) |

### Copilot

| Operation | File | API |
|---|---|---|
| Copilot license adoption | [`copilot/license_report.py`](./copilot/license_report.py) | [subscribedSku list](https://learn.microsoft.com/en-us/graph/api/subscribedsku-list) |
| Copilot usage (M365 apps report) | [`copilot/usage_report.py`](./copilot/usage_report.py) | [getM365AppUserCounts](https://learn.microsoft.com/en-us/graph/api/reportroot-getm365appusercounts) |
| Underused Copilot licenses | [`copilot/underused_licenses.py`](./copilot/underused_licenses.py) | [user list](https://learn.microsoft.com/en-us/graph/api/user-list) |

### Generic downloader

| Operation | File | API |
|---|---|---|
| Download any CSV report via `--report` | [`usage_reports.py`](./usage_reports.py) | [reportRoot](https://learn.microsoft.com/en-us/graph/api/resources/reportroot) |

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
