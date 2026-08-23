# OneDrive Drives

Explore and report on drives — personal OneDrive and SharePoint document
libraries — including tenant-wide storage reporting and per-user inspection.

---

## Prerequisites

| Permission | Description | Reference |
|---|---|---|
| `Files.Read` | Recent items, shared with me | [Files permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#files-permissions) |
| `Files.Read.All`, `Sites.Read.All` | All drives, storage, per-user drives (app) | [Files permissions](https://learn.microsoft.com/en-us/graph/permissions-reference#files-permissions) |

`explore.py` uses username/password; the reporting examples use client secret
with `require_application_permission(...)`.

---

## Examples

| Operation | File | API |
|---|---|---|
| Recent items, shared with me, followed sites | [`explore.py`](./explore.py) | [drive recent](https://learn.microsoft.com/en-us/graph/api/drive-recent) |
| Search a keyword across all drives | [`search_all.py`](./search_all.py) | [driveItem search](https://learn.microsoft.com/en-us/graph/api/driveitem-search) |
| Tenant-wide storage report (quota) | [`storage_report.py`](./storage_report.py) | [drive list](https://learn.microsoft.com/en-us/graph/api/drive-list) |
| A user's drive and quota | [`user_drive.py`](./user_drive.py) | [user drive](https://learn.microsoft.com/en-us/graph/api/user-list-drive) |

---

## API reference

- [Drive resource](https://learn.microsoft.com/en-us/graph/api/resources/drive)
- [Quota](https://learn.microsoft.com/en-us/graph/api/resources/quota)
