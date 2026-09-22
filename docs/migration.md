# Migration

Move content between Microsoft 365 and other systems — resumable, verifiable,
and with best-effort fidelity. The toolkit is product-agnostic (a `DataSource`
→ `DataTarget` pair) and ships adapters for the filesystem, SharePoint lists,
and SharePoint document libraries.

## The model

| Piece | Role |
|---|---|
| `DataSource` / `DataTarget` | adapters — `read`/`checksum` and `exists`/`write`/`list_paths` |
| `MigrationJob` | lifecycle `assess → plan → run → verify`, resumable |
| `Manifest` | the persisted plan (a list of `MigrationItem`) |
| `Checkpoint` | per-item status, incremental watermarks, phase (pause/resume/cancel) |
| `MigrationServerJob` | server-side Migration API ingestion (submit + monitor) |

## Quick start

Filesystem → SharePoint document library:

```python
from office365.migration import MigrationJob, MigrationOptions
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.sharepoint.adapters import SharePointLibraryTarget
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext(site_url).with_client_certificate(tenant, client_id, thumbprint, cert_path)
library = ctx.web.lists.get_by_title("Documents").root_folder

job = MigrationJob(
    FileSystemSource("src"),
    SharePointLibraryTarget(library),
    MigrationOptions(concurrency=4),
)
job.plan()
job.run()
print(job.stats.summary())
print(job.verify().summary())
job.export_reports("reports/")
```

Runs are **idempotent and resumable**: pass `manifest_path` / `checkpoint_path`
and a paused or failed run continues where it stopped (`job.resume()`). Set
`MigrationOptions(incremental=True)` to skip items at or below the persisted
watermark.

## Adapters

| Adapter | Direction | Content |
|---|---|---|
| `FileSystemSource` / `FileSystemTarget` | both | files + folders |
| `JsonFileSource` / `JsonFileTarget` | both | record payloads (one JSON file per item) |
| `SharePointLibrarySource` / `SharePointLibraryTarget` | both | files + folders (recursive) |
| `SharePointListSource` / `SharePointListTarget` | both | list items as records |
| `TeamsArchiveSource` / `TeamsArchiveTarget` | both | Teams archives |

## Fidelity

| Flag | Client-side runner | Server-side Migration API |
|---|---|---|
| `preserve_timestamps` | best-effort (`Created`/`Modified`) | full |
| `preserve_permissions` | best-effort (same-tenant ACL copy) | full |
| `preserve_versions` | ✗ (raises) | full |

REST cannot restore version history, so `preserve_versions` always requires the
server-side API. The other two are applied client-side **when the adapters
support them** — the runner fails fast otherwise, rather than silently migrating
without the requested fidelity:

```python
MigrationJob(source, target, MigrationOptions(preserve_timestamps=True, preserve_permissions=True))
```

- **Timestamps** — the SharePoint library target restores `Created`/`Modified`
  via `ValidateUpdateListItem` (the same path as `ListItem.system_update`).
- **Permissions** — the source reads the item's `role_assignments`; the target
  breaks inheritance and recreates them, resolving principals by login name and
  roles by name. This is a **same-tenant** copy; cross-tenant identity mapping is
  not implemented.

Adapters opt in by implementing optional hooks:
`DataSource.read_permissions(item)`, `DataTarget.apply_timestamps(item)`, and
`DataTarget.apply_permissions(item, permissions)`.

## Server-side migration (full fidelity)

For version history and true ACL fidelity, content is packaged and ingested
server-side. The package layer builds the Migration API manifest XML
(`Manifest.xml` / `ExportSettings.xml` / `SystemData.xml` / `UserGroupMap.xml`)
from a document library's files and folders:

```python
from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.sharepoint.package_target import SharePointPackageTarget

# Provision SharePoint-owned Azure containers (SAS URIs + encryption key)
containers = ctx.site.provision_migration_containers().execute_query().value

target = SharePointPackageTarget(
    ctx.site,
    web_id,
    content_uri=containers.DataContainerUri,
    manifest_uri=containers.MetadataContainerUri,
    encryption_key=containers.EncryptionKey,
)
job = MigrationJob(FileSystemSource("src"), target)
job.plan()
job.run()          # stages the package and submits the ingestion job
target.monitor()   # polls GetMigrationJobProgress
```

`MigrationServerJob` can also be driven directly (`submit` / `submit_encrypted` /
`progress` / `status_fn` / `monitor`).

The builder covers the **document-library subset** — webs, lists, folders, files,
and file versions. The generated XML follows the documented format but is **not
yet verified against a live tenant** (see `office365.migration.package`).

## Storage & vendor neutrality

Server-side ingestion is the only leg that needs Azure — and that is Microsoft's
requirement, not ours. The Migration API reads content/manifest blobs from Azure
Blob Storage; it cannot read from local disk or S3.

| Move | Path | Azure? | Fidelity |
|---|---|---|---|
| M365 → filesystem / S3 / other | client-side adapters | no | content + best-effort timestamps/ACLs |
| filesystem / other → M365 | client-side adapters | no | content + best-effort |
| filesystem / other → M365 | server-side Migration API | **yes** | versions, ACLs, authors |
| M365 → M365 | either | only for server-side | — |

### You don't need an Azure account

`Site.provision_migration_containers()` provisions **SharePoint-owned** containers —
*no extra cost, and without the need to manually set up in the Azure admin
console*. It returns the container URIs (with SAS tokens) and the encryption key.
The `[azure]` extra is **only the client library** used to push blobs into
whatever container you were handed — it is not an Azure subscription:

```bash
pip install office365-rest-python-client[azure]
```

### Step by step

```python
from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource
from office365.migration.sharepoint.package_target import SharePointPackageTarget

# 1. Provision SharePoint-owned containers (no Azure account needed)
containers = ctx.site.provision_migration_containers().execute_query().value
#    containers.DataContainerUri     -> content container (SAS)
#    containers.MetadataContainerUri -> manifest container (SAS)
#    containers.EncryptionKey        -> AES256CBC key

# 2. Point the target at the containers (staging is swappable — see below)
target = SharePointPackageTarget(
    ctx.site,
    web_id,
    content_uri=containers.DataContainerUri,
    manifest_uri=containers.MetadataContainerUri,
    encryption_key=containers.EncryptionKey,
)

# 3. Migrate: items -> manifest XML -> staged blobs -> submitted job
job = MigrationJob(FileSystemSource("src"), target)
job.plan()
job.run()
print(target.job_id)

# 4. Poll GetMigrationJobProgress until the job is terminal
target.monitor()
```

### The `Staging` seam

The package (documented XML + content blobs) is vendor-neutral bytes; **where they
land is a strategy**. Pass `staging=` to `SharePointPackageTarget`:

- `FileSystemStaging` — writes `manifest/` + `content/` to disk (no Azure; tests,
  inspection, or handing the package to another uploader);
- `BlobStaging` — Azure Blob (what `create_staging(...)` returns today);
- `create_staging(content_url, manifest_url)` — the factory that picks a backend by
  container host. It is the extension point: a future S3 / Azure Files staging
  slots in here without changing callers.

```python
from office365.migration.package import FileSystemStaging

# Build + write the package to disk (no Azure, no submit)
target = SharePointPackageTarget(
    ctx.site, web_id, staging=FileSystemStaging("pkg/content", "pkg/manifest")
)
package = target.stage()
```

### When you don't need Azure at all

If you don't need version history or ACLs, skip the package entirely and use the
client-side adapters — they move content over REST in either direction, including
to the filesystem (see [Fidelity](#fidelity)).

## Verification & reports

`job.verify()` reconciles item counts and spot-checks content checksums, and
`job.export_reports(dir)` writes Summary/Item/Failure reports as CSV + JSON.

## See also

- [Data pipeline](data-pipeline.md) — tabular import/export
- [Large lists](large-lists.md) — thresholds that shape a migration plan
- [Limits](limits.md) — the service limits the toolkit respects
