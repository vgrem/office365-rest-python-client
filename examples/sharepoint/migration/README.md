# Migration

Assess, migrate, monitor, and report using the migration toolkit — a resumable,
checkpointed migration layer (SPMT-style) built on the client and the data
pipeline. Works **into** SharePoint, **from** it, and between the filesystem /
records — directional (export/import).

Workflow mirrors SPMT: **scan/assess -> create a task -> monitor and report**.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the target site | Required to scan lists, files, and permissions. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Operation | File | Required role |
|---|---|---|
| Assess a site (site + subsites) for migration readiness | [`scanner.py`](./scanner.py) | Read access |
| Bulk-assess a list of sites | [`scanner_bulk.py`](./scanner_bulk.py) | Read access |
| Copy a local directory tree (filesystem → filesystem) | [`migrate_files.py`](./migrate_files.py) | none (local) |
| Export a SharePoint list to local JSON records | [`export_list_to_json.py`](./export_list_to_json.py) | Read access |
| Export a document library to local files | [`migrate_library.py`](./migrate_library.py) | Read access |
| Migrate a tree and write Summary/Item/Failure reports | [`export_reports.py`](./export_reports.py) | none (local) |

---

## Quick start

### 1. Scan and assess (Step 2)

```python
from office365.migration import MigrationAssessor
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)
report = MigrationAssessor(ctx.web).include_permissions().assess(recursive=True).execute_query().value
print(report.summary())          # Webs/Lists/Files/Size + blockers/warnings + ready
print(report.to_records())       # issues as records (CSV/JSON export)
```

### 2. Create a migration task and run (Step 3)

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
```

### 3. Monitor and report (Step 4)

```python
job.export_reports("reports")            # SummaryReport / ItemReport / FailureReport (CSV + JSON)
print(job.verify().summary())            # reconcile source vs target
```

### Incremental re-runs

Set `incremental=True` (with `OVERWRITE` conflict resolution) to copy only items
whose source is newer than the target — SPMT-style:

```python
from office365.migration import MigrationJob, MigrationOptions, ConflictResolution

job = MigrationJob(
    FileSystemSource("src"),
    FileSystemTarget("dst"),
    options=MigrationOptions(incremental=True, conflict_resolution=ConflictResolution.OVERWRITE),
)
```

---

## API reference

- [SharePoint Migration API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference)
- [SharePoint Migration Tool (SPMT) overview](https://learn.microsoft.com/en-us/sharepointmigration/introducing-the-sharepoint-migration-tool)
