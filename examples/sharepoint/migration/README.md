# Migration

Assess, migrate, and verify using the migration toolkit — a resumable,
checkpointed client-side migration layer (SPMT-style) built on the client and
the data pipeline. Works both **into** SharePoint and **from** it.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the target site | Required to scan lists, files, and permissions. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Operation | File | Required role |
|---|---|---|
| Assess a site for migration readiness | [`scanner.py`](./scanner.py) | Read access |
| Copy a local directory tree (filesystem -> filesystem) | [`migrate_files.py`](./migrate_files.py) | none (local) |
| Export a SharePoint list to local JSON records | [`export_list_to_json.py`](./export_list_to_json.py) | Read access |

---

## Quick start

### 1. Assess (the "scan" phase)

```python
from office365.migration import MigrationAssessor
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)
report = MigrationAssessor(ctx.web).include_permissions().assess().execute_query().value
print(report.summary())          # blockers / warnings
print(report.blockers)
```

### 2. Migrate (the "run" phase) - filesystem -> filesystem

```python
from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget

job = MigrationJob(
    FileSystemSource("src"),
    FileSystemTarget("dst"),
    checkpoint_path="checkpoint.json",   # enables pause/resume
)
job.plan()
job.run()
print(job.stats.summary())
print(job.verify().summary())
```

### 3. Export a list from SharePoint (JSON records)

```python
from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import JsonFileTarget
from office365.migration.adapters.sharepoint import SharePointListSource

job = MigrationJob(SharePointListSource(ctx.web.lists.get_by_title("Contacts")), JsonFileTarget("out"))
job.plan(); job.run()
print(job.verify().summary())
```

---

## API reference

- [SharePoint Migration API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference)
