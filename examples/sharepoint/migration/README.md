# Migration

Assess a SharePoint site for migration readiness using the SharePoint
Migration API.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the target site | Required to scan lists, versions, and permissions. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Operation | File | Required role |
|---|---|---|
| Run a migration assessment (permissions + versions) | [`scanner.py`](./scanner.py) | Read access |

---

## Quick start

```python
from office365.migration.assessor import MigrationAssessor
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)
report = MigrationAssessor(ctx.web).include_permissions().include_versions().assess().execute_query()
print(report.value.summary())
```

---

## API reference

- [SharePoint Migration API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference)
