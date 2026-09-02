# Migration

Assess, migrate, monitor, and report using the migration toolkit — a resumable,
checkpointed migration layer built on the client and the data pipeline. Works
**into** SharePoint, **from** it, and between the filesystem / records —
directional (export/import).

Workflow: **scan/assess -> create a task -> monitor and report**.

---

## Prerequisites

| Requirement | Description | Reference |
|---|---|---|
| **Read access** to the target site | Required to scan lists, files, and permissions. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |
| **SharePoint admin** (for tenant-scope scans) | `scan_large_sites.py` enumerates site collections via the SPO.Tenant API — SMAT's farm-account prerequisite. | [SharePoint admin roles](https://learn.microsoft.com/en-us/sharepoint/sharepoint-admin-role) |

---

## Examples

| Operation | File | Required role |
|---|---|---|
| Assess a site (site + subsites) for migration readiness | [`scanner.py`](./scanner.py) | Read access |
| Bulk-assess a list of sites | [`scanner_bulk.py`](./scanner_bulk.py) | Read access |
| Generate the SMAT `LargeSites-detail.csv` report (all tenant sites over 500 GB) | [`scan_large_sites.py`](./scan_large_sites.py) | SharePoint admin |
| Copy a local directory tree (filesystem → filesystem) | [`migrate_files.py`](./migrate_files.py) | none (local) |
| Export a SharePoint list to local JSON records | [`export_list_to_json.py`](./export_list_to_json.py) | Read access |
| Export/import a document library ↔ local files (`--import`, `--concurrency`) | [`migrate_library.py`](./migrate_library.py) | Read/Write access |
| Migrate local files into a library via a migration session (parallel) | [`migrate_session.py`](./migrate_session.py) | Write access |
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
print(report.scan_reports["LargeSites"].records)   # SMAT-style scan detail
```

### Scan reports (SMAT roadmap)

The assessment is modular — scans are registered in
`office365.migration.assessment.registry` (a ScanDef.json analog: name,
scanner, `ReportCategoryType`, `Enabled`, properties). Each scan emits an
SMAT-style detail report (`ScannerReports/<Scan>-detail.csv` + `.json`) and can
flag issues on the assessment report.

```python
from office365.migration.assessment.registry import SCANS
from office365.migration.assessment.export import export_assessment

print([d.name for d in SCANS])                      # the registered scans
written = export_assessment(report, "out")          # issues + ScannerReports/
```

**Large Sites** (SPSite, on by default) validates site size against the 500 GB
guidance and reports the SMAT columns (SiteId, SiteURL, SiteOwner,
SiteSizeInMB, NumOfWebs, LastContentModifiedDate, TotalItemCount, Hits,
SizeInGB, ...). On-prem-only fields (`ContentDB*`, usage-logging metrics)
report `n/a`. Disable it or any scan with `--disable-scan LargeSites` /
`assessor.disable_scan("LargeSites")` — the assessor then skips collecting its
data.

Run it at **tenant scope** (SMAT model: enumerate site collections first, then
report the large ones) with `MigrationTenantAssessor`:

```python
from office365.migration import MigrationTenantAssessor
from office365.sharepoint.tenant.administration.tenant import Tenant

report = MigrationTenantAssessor(Tenant(admin_client)).assess().execute_query().value
scan = report.scan_reports["LargeSites"]
print(scan.to_csv())   # SMAT LargeSites-detail.csv (typed rows -> trivial export)
```

Each scan report has a typed row model — the dataclass fields are the SMAT
column headers — so `to_records()` / `to_json()` / `to_csv()` are one-liners
and `None` renders as `n/a`.

Implemented | SMAT roadmap scans (planned)
--- | ---
Large Sites, Locked Sites | Large Lists, Large List Views, Large Excel Files, Checked-out files, File Versions, Long OneDrive URLs, Unsupported Site Templates, Workflow Associations (2010/2013), ... (see the [SMAT scan reports roadmap](https://learn.microsoft.com/en-us/sharepointmigration/sharepoint-migration-assessment-toolscan-reports-roadmap))

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
whose source is newer than the target:

```python
from office365.migration import MigrationJob, MigrationOptions, ConflictResolution

job = MigrationJob(
    FileSystemSource("src"),
    FileSystemTarget("dst"),
    options=MigrationOptions(incremental=True, conflict_resolution=ConflictResolution.OVERWRITE),
)
```

### Parallel migration & sessions (fast)

File bytes **cannot ride an OData batch** — SharePoint doesn't support batched file
uploads — so throughput comes from **concurrency**: `MigrationOptions.concurrency`
spins up parallel workers, each on a cloned `ClientContext` (reusing auth +
transport), all sharing one `RateLimiter` that paces the fleet on
`Retry-After` / `X-SharePointHealthScore`. The library target applies this via
its `write_many` fast path over the *deferred* `upload_file`/`upload_content`
primitives. Record/list writes use the JSON-only
`execute_batch(items_per_batch=…, concurrency=…)` instead.

```python
from office365.migration import MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.adapters.sharepoint import SharePointLibraryTarget

job = MigrationJob(
    FileSystemSource("src"),
    SharePointLibraryTarget(library_folder, concurrency=4),
    options=MigrationOptions(concurrency=4),
)
job.plan()
job.run()
```

A `MigrationSession` coordinates a **batch of migrations** — each task is a
source → target `MigrationJob` added explicitly, then started together:

```python
from office365.migration import MigrationOptions, MigrationSession

session = MigrationSession()
session.add_task(
    FileSystemSource("src-a"),
    SharePointLibraryTarget(library_a, concurrency=4),
    options=MigrationOptions(concurrency=4),
)
session.add_task(
    FileSystemSource("src-b"),
    SharePointLibraryTarget(library_b, concurrency=4),
    options=MigrationOptions(concurrency=4),
)
session.start()
print(session.status())
```

A single migration needs no session — `MigrationJob(source, target, options)`
with `plan()`/`run()`/`verify()` is the primary entry point.

---

## API reference

- [SharePoint Migration API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference)
- [SMAT scan reports roadmap](https://learn.microsoft.com/en-us/sharepointmigration/sharepoint-migration-assessment-toolscan-reports-roadmap)
- [Large Sites scan](https://learn.microsoft.com/en-us/sharepointmigration/migration-assessment-scan-large-sites)
- [Locked Sites scan](https://learn.microsoft.com/en-us/sharepointmigration/migration-assessment-scan-locked-sites)
