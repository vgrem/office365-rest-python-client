# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Typed CAML query builder:** `Caml` / `CamlQuery.builder()` construct `ViewXml`
  from composable Python expressions instead of raw CAML strings — fluent
  comparisons (`Caml.text("Status").eq("Active")`), field-typed helpers
  (`Caml.lookup("Category").id().in_([2, 3])`), value nodes (`Caml.now`), logical
  joins (`.and_()/.or_()/.not_()`, `&`/`|`/`~`, variadic `Caml.and_/or_`) that
  always render **binary-nested** CAML, plus
  `where/order_by/group_by/row_limit/scope/view_fields`. Raw `ViewXml`/`parse`
  remain supported. New modules under `office365/sharepoint/listitems/caml/`
  (`values`, `fields`, `expressions`, `builder`); removed the unused `types` stubs.
- `ImportResult` — a deferred, source-agnostic streaming import driver. Chunks
  are queued, executed, and discarded (bounded memory), and the caller picks the
  terminal: `execute_query()` (sequential), `execute_batch(...)` (server-side,
  concurrent), or iterating the driver. `ClientObjectCollection.import_records()`
  streams record batches; `List.from_dataframe()` streams a DataFrame / CSV
  source and provisions the columns once.
- **Idempotent list imports (skip / upsert):** `List.import_dataframe(..., key=...,
  key_field="MigrationKey", on_conflict="skip"|"upsert")` derives a SHA-256 key
  from the given natural-key column(s), stores it in a dedicated field, loads the
  existing keys once, and skips or updates already-present rows — so a re-run
  never duplicates. Backed by `runtime.converters.upsert.keyed_queue` +
  `ListItemUpsertTarget` and a conflict-resolution `queue` hook on `ImportResult`
  (`ImportStats.skipped`); `enforce_unique=True` and `dry_run=True` are supported.
- **Resumable imports:** `ImportResult` accepts a `checkpoint` — a path
  (`FileCheckpointStore`), an `ImportCheckpoint`/`None` (`MemoryCheckpointStore`),
  or any `CheckpointStore` — and persists the committed cursor after each chunk
  (atomically), so an interrupted long-running run resumes by skipping the
  already-committed chunks. `ImportResult.resumed_from`/`.checkpoint` and
  `ImportStats.resumed_from` (in `summary()`) expose the resumed offset.
  `on_error="collect"` records a failing chunk (`ImportStats.errors` +
  `checkpoint.failures`) and continues instead of aborting.
- `ClientObjectCollection.clear()` and a `concurrency` argument on
  `Entity.execute_batch()`.
- `OperationStats` — a shared counter base for bulk operations — with
  `ImportStats` and `MigrationStats` as specializations (no lossy conversion
  between them).
- **Live import progress:** the `progress` hook now fires immediately (with the
  resumed offset, so a bar appears with its total) and then per committed chunk
  *and per completed batch* during `execute_batch`, instead of only once per
  queued chunk. `run_parallel` reports progress on the calling thread as tasks
  complete (the completed result in `Progress.items`), and `execute_batch`'s
  `success_callback` now fires per batch in sequential mode too (it previously
  never fired there). `List.import_from(..., total=...)` lets callers supply the
  known total so the progress percentage/ETA is meaningful.
- **Best-effort migration fidelity:** the migration runner now applies
  `preserve_timestamps` / `preserve_permissions` client-side when the adapters
  support it, via new optional hooks `DataSource.read_permissions(item)` /
  `DataTarget.apply_timestamps(item)` / `DataTarget.apply_permissions(item,
  permissions)` (with `PermissionEntry`). The SharePoint library adapters restore
  `Created`/`Modified` through `ValidateUpdateListItem` and recreate the source
  role assignments (same-tenant).
- **Migration guide:** `docs/migration.md` documents the adapter/job model,
  fidelity tiers, and the server-side ingestion path.
- **Server-side migration (full fidelity):** new `Site` methods
  `provision_migration_containers`, `provision_migration_queue`,
  `create_migration_job_encrypted`, and `get_migration_job_progress`.
  `MigrationServerJob` gained `submit_encrypted`, `progress`, and a
  `GetMigrationJobProgress`-backed `status_fn` (`monitor` now defaults to it);
  `parse_progress_events` reduces the event log to `(status, done, total)`.
- **Migration API package layer** (`office365.migration.package`): models and
  serialization for `Manifest.xml` / `ExportSettings.xml` / `SystemData.xml` /
  `UserGroupMap.xml`, a `PackageBuilder` (deterministic GUIDs, folders, files,
  versions; indented XML), `FileSystemStaging`, and optional `BlobStaging` (new `[azure]` extra:
  `azure-storage-blob`; `AzureBlobStaging` kept as an alias). `create_staging(...)`
  selects a backend from the container URL — the seam for a future S3 / Azure
  Files staging. `SharePointPackageTarget` ties it together as a `DataTarget` — it
  builds the package, stages the blobs, and submits an ingestion job (the
  constructor accepts `staging=` alone, so a package can be built and staged
  without Azure). Covers the **document-library subset**; the generated XML
  follows the documented format but is **not yet verified against a live tenant**.
- **Storage & vendor-neutrality docs:** `docs/migration.md` now covers which legs
  need Azure (only the server-side SharePoint ingest leg, and containers can be
  SharePoint-provided — no Azure account), the `Staging` seam, and a step-by-step
  example.
- **Encrypted migration staging:** `BlobStaging` / `create_staging` accept an
  `encryption_key`; every content and manifest blob is then AES-256-CBC encrypted
  (unique random IV, stored as the base64 `IV` blob property) — required for
  SharePoint-provided containers. `SharePointPackageTarget` forwards its
  `encryption_key` to the default staging, and the `[azure]` extra now also pulls
  in `cryptography`.
- **Migration examples:** `migrate_library_serverside.py` is a five-step,
  zero-argument server-side migration (defaults to the repo sample data), and a
  new tenant-free `package_library.py` builds the same package offline so the
  manifest XML can be inspected. The migration README now explains the pipeline,
  which example to run, and in what order.
- **SPMT-style migration sessions:** `MigrationSession` now mirrors the
  `Microsoft.SharePoint.MigrationTool.PowerShell` cmdlets — `register` / `get` /
  `add_task` / `remove_task` / `show` / `start` / `stop` (cancel) / `unregister`,
  with task ids. New `MigrationSettings` (the `Register-SPMTMigration` surface,
  mapped to `MigrationOptions` via `to_options()`) and `MigrationTask`
  (`FileShare`/`SharePoint` descriptors + the SPMT JSON task format). A SharePoint
  resolver builds the adapters from a task descriptor — client-side REST by
  default, or the server-side Migration API with `use_migration_api=True`.
  `MigrationOptions` gained `created_after`/`modified_after` date filters.

### Changed
- **Data-pipeline naming (breaking):** `from_*` is now the **streaming** entry
  (returns `ImportResult`) and `queue_*` (`queue_records`/`queue_dataframe`) is
  the deferred queue-all path. Removed `import_from`/`import_records`/
  `import_dataframe`/`import_from_file` (use `from_records`/`from_dataframe`/
  `from_file`) and `to_json_file`/`from_json_file` (use `export_to(..., format=
  "json")`/`from_json`). `FieldCollection.from_dataframe` →
  `ensure_from_dataframe`; the JSON-array file format is registered as `json`
  (`json_file` kept as an alias).
- **Architecture:** the data-interchange surface (pandas/CSV/JSON/NDJSON/Excel
  import/export) moved off the core `ClientObjectCollection` onto a new
  `RecordCollection` base (inherited by every typed `EntityCollection`). Formats
  are resolved through `runtime.converters.registry`; unified `export_to(...)` /
  `import_from(...)` sit alongside the existing `to_*`/`from_*` conveniences.
  Keyed skip/upsert is a pluggable `UpsertTarget` (`runtime.converters.upsert`)
  implemented for list items by `ListItemUpsertTarget`; the migration toolkit's
  `SharePointListTarget` reuses it.
- `import_from`/`import_records` gained `enforce_unique=True` (mark the key column
  unique) and `dry_run=True` (plan the create/update/skip counts without writing).
- `List` gained record facades over its items: `import_from`/`import_dataframe`/
  `import_records` (streaming), `export_to`/`to_dataframe` (record export). The
  naming is now consistent everywhere: `from_*` is deferred (queue-all),
  `import_*` is the streaming `ImportResult`. `List.from_dataframe` is now
  **deferred** (it was the streaming entry); use `List.import_dataframe` for the
  streaming path. `List.export` remains the `.zip` **package** export.
- `SharePointListSource` now reuses the shared record projection
  (`to_records(raw=True)`, no JSON coercion).
- `MigrationOptions.preserve_timestamps` now defaults to `False` (it was `True`
  but never implemented). `preserve_timestamps`/`preserve_permissions` are
  applied client-side on a best-effort basis (see above); `preserve_versions`
  still needs the server-side Migration API (`MigrationServerJob`). Enabling a
  flag the adapter pair can't honor raises `NotImplementedError` instead of
  silently no-op'ing.
- `Site.create_migration_ingestion_job` — `azure_queue_report_uri` and
  `ingestion_task_key` are now optional (the API treats the queue as optional).
- **Streaming export + row-level dead-letter:** `export_to(..., page_size=...)`
  streams appendable formats (CSV/TSV/NDJSON/JSON) page by page — bounded memory
  for large collections. With `on_error="collect"` **and** a `dead_letter`, a
  chunk is executed record-by-record so each failing row is dead-lettered as
  `{"row": ..., "error": ..., "record": {...}}`.
- **Large-list threshold mitigations:** a typed
  `SPQueryThrottledException` with actionable guidance; `Folder.get_files` now
  pages (so >5,000-item folders work — refs #930/#936/#462);
  `List.get_items(query, page_size=...)` pages CAML results (continuing from the
  last item via `ListItemCollectionPosition`); `List.ensure_indexed(name)` /
  `Field.ensure_indexed()` index an existing column via `enableIndex` (the real
  fix for #427); and `List.get_items` warns on unpaged filter/sort queries. New
  `docs/large-lists.md` guide (including the large-library upload caveat, #726).
- **Large-list UX:** list-view-backed collections (`ListItemCollection`,
  `FileCollection`, `FolderCollection`) now **warn once** when an unpaged load
  reaches the 5,000-item threshold (they may have been silently trimmed) and point
  at the paged API — covering the `ctx.load(folder, ["Files"])` path from
  #930/#936. `CamlQuery.index_candidates` / `List.index_candidates(query)` name the
  columns a query should index (propose, never mutate). `List.check_query(query)`
  (and `List.get_items(query, ..., check=True)`) pre-flights a query and raises
  actionable guidance naming the columns to index instead of the opaque server
  500 (opt-in; performs 1–2 requests).
- **Migration-parity vocabulary:** `ImportResult.run(...)` aliases
  `execute_batch`, and `ImportResult.verify(source, key=...)` reconciles a
  source's natural keys against the target (delegating to the collection). The
  pipeline and the migration toolkit now share one `VerificationReport`
  (`runtime.verification`); `RecordCollection.verify` / `List.verify` generalize
  `verify_keys` / `verify_dataframe`.
- **More formats + path/IO parity:** the pipeline now supports `tsv`, `parquet`,
  `orc` and `feather` (optional `[parquet]` extra) alongside CSV/JSON/NDJSON/
  Excel/DataFrame, plus `from_sql`/`to_sql` (`[sql]`) and `from_duckdb`/
  `to_duckdb` (`[duckdb]`) for bounded-memory DB streaming. Every reader/writer
  accepts a path, a `PathLike` **or** an open file object (pandas parity); the
  JSON-array file format is registered as `json` (`json_file` alias kept).
- **DataFrame ⇄ SharePoint file bridge:** `Folder.write_dataframe("stocks.csv",
  df)` / `File.write_dataframe(df)` serialize a DataFrame into a file's
  **content** (UTF-8-BOM CSV so Excel keeps the columns, XLSX, JSON, ...), and
  `Folder.read_dataframe("stocks.csv")` / `File.read_dataframe()` parse a file's
  content back into a DataFrame (deferred `DataFrameResult`). File **metadata**
  stays as plain properties. `List.from_file("Shared Documents/stocks.csv",
  key=...)` downloads a SharePoint-hosted CSV/XLSX and streams it into the list
  (bounded, resumable, idempotent). `dataframe_to_bytes`/`dataframe_from_bytes`
  are the content codecs.
- **Typed field mapping on import:** `List.import_from(..., schema={column:
  FieldType})` now also **coerces values** into the payload shape SharePoint
  expects — MultiChoice (`"; "`-separated or a list), Lookup/MultiLookup,
  User/MultiUser (`{LookupId}`/`{Email}`), URL (`{Url, Description}`),
  Geolocation, plus Boolean/Integer/Number/DateTime parsing. Backed by
  `office365.sharepoint.fields.coercion.coerce_field_value`; the generic
  `RecordCollection.import_from(..., coerce={key: converter})` hook keeps the
  runtime destination-agnostic.
- **Column mapping:** `import_from(..., mapping={"SourceCol": "TargetField"})`
  renames source columns/keys before queuing (list imports rename before
  field-name sanitization), so differently-named sources land in the right columns.
- **Import verification:** `RecordCollection.verify_keys(keys)` reconciles a keyed
  import against the target (returns a `VerificationResult` with `ok`/`missing`);
  `List.verify_dataframe(df, key=...)` derives the keys from a DataFrame.
- **Dead-letter capture:** `ImportResult`/`import_from(..., dead_letter="dl.jsonl")`
  appends each collected chunk failure (`{"error": ..., "records": [...]}`) to a
  JSONL file (with `on_error="collect"`) for remediation.
- **Import schema evolution:** `List.import_from(..., on_schema_change="evolve"|
  "fail")` provisions columns that first appear in a later chunk (default
  ``evolve``) or rejects them (``fail``); backed by a per-chunk ``before_chunk``
  hook on `ImportResult` that runs before the chunk is queued.
- **Incremental migration watermark:** `MigrationRunner` now uses the persisted
  `Checkpoint.source_watermark` — with `MigrationOptions.incremental` it skips
  items at/below the watermark and advances it to the highest migrated source
  `modified` (filesystem, SharePoint library and list sources populate it), so a
  resumed incremental run only re-scans new/changed items.
- Removed `office365/migration/_util.py`; its helpers moved to their domains:
  `emit_progress` → `runtime.operations`, `iso`/`iso_or_none`/`utc_now_iso` →
  `runtime.converters.scalars`, `record_to_json` → `runtime.converters.json_file`.
  Report writing is now **per-format** (`migration.report_io.write_dataset`/
  `write_formats`) instead of the CSV+JSON-coupled `write_csv_json`.
- `MigrationItem` carries `created` and the reliable system `author_id`/`editor_id`
  (in addition to `modified`); the filesystem, SharePoint library and SharePoint
  list sources populate them, and the item report exports them. Incremental
  migration now has source timestamps for SharePoint libraries, and
  `SharePointLibraryTarget.modified()` supports the target-side comparison.
- **Idempotent metadata:** all client-side `ensure_*` (fields, lists, content
  types, terms, contact folders) share new
  `runtime.queries.get_or_create.get_or_create`/`create_or_get` primitives, and
  accept `on_conflict="skip"|"update"` to reconcile an existing definition.
- `List.ensure_field`/`ensure_fields` and `FieldCollection.from_dataframe`
  now return the ensured **entity/entities** (`Field` / `list[Field]`);
  `Folder.ensure_folders` returns `list[Folder]`. `List.ensure_fields_from_dataframe`
  was removed (use `List.fields.from_dataframe`).
- **Breaking:** `List.from_dataframe()` returns an `ImportResult` driver instead
  of the `List`; `progress` is now keyword-only and the whole frame is no longer
  queued — execution happens on the chosen terminal.
- The SharePoint list migration target flushes each chunk and discards the
  queued entities, keeping large record migrations memory-bounded.

### Fixed
- **Server-side file imports need a matching `SPListItem` (live-validated).** The
  Migration API **silently skips** an `SPFile` unless the package also contains
  the file's `SPListItem` (with a `<Fields>` member) — `PackageBuilder.add_file`
  now emits it, and `add_list_item` reuses it for sharing metadata. Also: every
  `<User>` must carry `SystemId` (the service schema requires it although the docs
  call it optional), and `DeploymentRoles` must **not** be emitted (the target's
  role definitions already exist — *"Updates to system roles is not allowed"*).
- **`PackageBuilder.add_role_assignment` now defaults `object_type="2"`.** The
  service parses `RoleAssignment/@ObjectType` as a numeric enum (`0` web, `1`
  list, `2` item/file); `2` was live-validated to break inheritance on a file.
  Note: the grant itself (`Assignment` role→principal) and `Author`/`ModifiedBy`
  still don't land — the target user's `SystemId` (SID) isn't exposed by the SPO
  REST API, so the principal can't be resolved yet (parked).
- **On-prem NTLM auth works again (refs #1045).** `ClientContext(url, allow_ntlm=True)`
  was ignored twice over: `with_user_credentials` raised unconditionally instead of
  delegating to `AuthenticationContext.with_credentials` (which already routes to
  `NtlmProvider` when `allow_ntlm` is set), and `pending_request()` never forwarded
  `allow_ntlm`/`browser_mode` to the request. `with_user_credentials` now delegates,
  the flags are forwarded, and the retired-SAML guard still fires for SharePoint
  Online (`allow_ntlm=False`).
- **`SharePointPackageTarget` no longer emits an empty `ExportSettings` `SiteUrl`.**
  It fell back to an unloaded `site.url` (`None` → `""`), so the API rejected the
  job with `There is an error in XML document (2, 62)` /
  `Invalid URI: The URI is empty.` The target now resolves the site URL (loading
  `Url` when needed) or raises a clear error, and accepts a `source_type`.
- **`Manifest.xml` now matches the shape the service accepts.** It emitted a
  `SPWeb` object (rejected — the service's `SPObjectType` excludes it) and a
  `<List>` element. Following the working `MigrationApiDemo` sample it now emits
  the library **root `SPFolder`**, the **`SPDocumentLibrary`**, an `SPFolder` per
  subfolder, and an `SPFile` per file — with `FileValue` = the content blob name
  (so the manifest points at the staged blobs) and `ListItemIntId`. Also fixed
  `UserGroupMap.xml` → **`UserGroup.xml`** (the name the API downloads) and the
  `ViewFormsList` namespace (`…viewformlist…`, not `…viewformslist…`).
- **Migration packages now emit the manifest files the API fetches.** The
  ingestion service downloads `Requirements.xml` / `RootObjectMap.xml` /
  `LookupListMap.xml` / `ViewFormsList.xml` by name, and a missing one fails the
  job (`Unable to download Requirements.xml … (404)`) even though the docs call
  them optional. `PackageBuilder` emits all four (childless roots, plus a `List`
  entry in `RootObjectMap.xml`). Failed jobs are now diagnosable:
  `MigrationServerJob.all_events` / `errors`, `SharePointPackageTarget.events` /
  `errors` / `diagnose` (which fetches and AES-decrypts the API's import log via
  `BlobStaging.read_manifest_blob`).
- **`CreateMigrationJobEncrypted` sends the AES key as base64 text.**
  `provision_migration_containers()` returns the key already base64-encoded, and
  the REST payload wants that base64 string — so `create_migration_job_encrypted`
  now passes a `str` key through (base64-encoding raw `bytes`) instead of decoding
  it. Decoding produced raw bytes that the payload serializer tried to UTF-8-decode
  (`UnicodeDecodeError`).
- **`$skip` paging no longer collides with a server `$skiptoken`.** Once the
  server drives paging (`__next`/`@odata.nextLink`), the client-side `$skip`
  fallback is disabled, fixing `The $skip and $skiptoken cannot be specified at
  the same time` on the final page of a paged collection (e.g.
  `items.order_by("ID").get_all(page_size=2000)`).
- **Idempotent imports now load existing keys on every run**, not only on a fresh
  one. A resumed run previously skipped the key load (it lived in the fresh-only
  `prepare` hook), so a replayed or overlapping chunk (a crash between the server
  commit and the checkpoint write, or a changed `--chunk`) could duplicate rows.
  The key column is ensured and the existing keys are loaded lazily before the
  first queued chunk — fresh or resumed — so `key=...` imports are idempotent on
  every run. `ImportCheckpoint` also records a source signature (format, chunk
  size, key columns); on a mismatch the chunk-based skip is discarded and the
  source is re-scanned (the keyed skip keeps it duplicate-free).
- DataFrame import no longer silently drops a column whose title collides with a
  built-in SharePoint field (e.g. `Name` resolves to `FileLeafRef`): the column
  is imported with a `_` suffix and a warning is emitted.
- `series_kind`/`field_type_from_kind` now handle complex, timedelta, category
  and object-datetime columns, and unknown kinds fall back to `Text` instead of
  raising `KeyError`.

## [3.1.1] - 2026-09-13

### Fixed
- SharePoint form digest is cached correctly again (`_valid_from` is set when
  the digest is fetched) and refreshed with a safety margin, so
  `/_api/contextInfo` is no longer requested on **every** call — it is fetched
  once per site/run and pre-warmed before parallel `execute_batch`, which
  removes the throttling (`429`) storm seen on long batch imports.
- A throttled digest refresh (`429`/`503`) is now retried honoring
  `Retry-After`, and an expired/invalidated digest (`403`, security validation)
  is refreshed and the affected request retried once. The error is surfaced as
  `SecurityValidationException` (`office365/sharepoint/exceptions.py`),
  dispatched by `ClientRequestException.from_response` via a registry so the
  runtime stays product-agnostic.
- Whole-batch throttling (`429`/`503`) now honors `Retry-After` instead of
  falling back to exponential backoff.
- `File.open_binary` / `File.save_binary` mangled the URL by percent-encoding
  the whole OData call (`(`→`%28`, `)`→`%29`, `$`→`%24`) and adding a stray
  backslash before `$value`, causing a `400 Bad Request`
  ([#978](https://github.com/vgrem/office365-rest-python-client/issues/978)).
  Only the path value is encoded now; the call syntax and `/$value` stay
  literal.

## [3.1.0] - 2026-09-13

### Added
- **Migration toolkit** — product-agnostic core plus `sharepoint`, `outlook`
  and `teams` products: resumable `MigrationJob`/`MigrationSession` with
  checkpoints, filesystem/SharePoint/JSON/Teams archive adapters, parallel
  transfer, a server-side ingestion job, and summary/item/failure reports.
- **SMAT-style pre-migration assessment** — modular scans/containers,
  `MigrationAssessor`/`MigrationTenantAssessor`/`MailboxAssessor`, typed scan
  reports (`LargeSites`, `LockedSites`, `MailFolders`) and CSV/JSON export.
- **Parallel execution** — `execute_batch(concurrency=N)` on `ClientContext`
  and `GraphClient`, plus `execute_query_parallel(concurrency=N)` for
  pipelined I/O over independent queries; both retry transient failures per
  request honoring `Retry-After`.
- **Data pipeline** — CSV/JSON/NDJSON/Excel import-export,
  `from_csv`/`from_json`/`from_records`, dynamic list-item columns, and an
  optional pandas bridge (`to_dataframe`/`from_dataframe`).
- **SharePoint** — taxonomy term store (OData v2.1/V4) support, site
  primitives, folder download with version history, zip ↔ folder primitives,
  `Web.ensure_list`, `DriveItem.ensure_folder`, and typed field creators.
- **Generator** — OData function/action method generation, a return-type
  descriptor/resolver, and list-typed primitive collection parameters.

### Changed
- Thread-safe auth and form-digest caches (single-flight refresh);
  `ClientContext.clone` now shares the auth context and transport.
- First-class retry (exponential backoff + jitter) and throttling
  (rate-limit/health headers) primitives; `ClientQuery` generics made
  consistent.
- Examples reorganized into product galleries and an SPMT-style migration flow
  (`assess/` → `migrate/` → `monitor/`).

### Fixed
- Long file paths in moves ([#988](https://github.com/vgrem/office365-rest-python-client/issues/988)) —
  body-based `File.move_by_path`/`MoveCopyUtil.move_file_by_path`; slashes are
  no longer percent-encoded inside OData string literals.
- Bulk OneDrive downloads ([#881](https://github.com/vgrem/office365-rest-python-client/issues/881)) —
  `download_folder` paginates children instead of stopping at the first page.
- SharePoint paging falls back to `$skip` when no next link is returned
  ([#915](https://github.com/vgrem/office365-rest-python-client/issues/915)),
  and custom headers are preserved across pages.
- Apostrophes in file paths ([#884](https://github.com/vgrem/office365-rest-python-client/issues/884)),
  in-memory upload streams ([#793](https://github.com/vgrem/office365-rest-python-client/issues/793)),
  sharing-token UTF-8/padding ([#875](https://github.com/vgrem/office365-rest-python-client/issues/875)).
- `@odata.type` casting for directory collections
  ([#921](https://github.com/vgrem/office365-rest-python-client/issues/921));
  principal path precedence ([#895](https://github.com/vgrem/office365-rest-python-client/issues/895));
  delta-token/custom query-param handling ([#948](https://github.com/vgrem/office365-rest-python-client/issues/948));
  malformed JSON surfaced as `ClientRequestException`.

### Internal
- Generator metadata readers/model moved from `office365/runtime/odata` to
  `generator/odata`; generator checkpoints are no longer tracked.
- Unit suite consolidated into themed modules and pruned; pyright clean.

## [3.0.0]

### Breaking
- **Python 2 dropped** — minimum Python version is now 3.8
- **ACS/SAML retirement** — `with_user_credentials` now raises `RuntimeError` for SharePoint Online. Use `with_username_and_password` (MSAL ROPC) instead. ACS App-Only (`with_client_credentials`) marked as deprecated.
- **USGovernment GCC endpoints corrected** — were using wrong URLs
- Model surface updated across SharePoint, Graph, and security namespaces (see Removed below)

### Added
- Full type hints across all modules (runtime, directory, onedrive, outlook, teams, sharepoint, intune, and more)
- `with_username_and_password` (MSAL ROPC) for SharePoint Online auth
- Substantially expanded Graph model coverage: Defender/security evidence types, subject rights requests, retention labels, threat intelligence, and more
- Expanded Intune (Cloud PC) and Teams admin/communication model surface
- New query/example modules for SharePoint, Graph, and Entra ID scenarios

### Changed
- Modernized SharePoint models and generator with Python 3 type hints (`Self`, `X | None`)
- `datetime.utcnow()` replaced with timezone-aware alternatives (Python 3.12+ deprecation)
- Generator tooling: `entity_type_name` support, EnumType generation, template-driven model props
- Credential/guard improvements for Entra ID multi-resource (via `ResourceName`)

### Fixed
- Cryptography CVEs updated to 48.0.0
- Circular import in `client_runtime_context.py` / `read_entity.py`
- `NameError: name 'List' is not defined` in `fields/collection.py`
- `single()` and `first()` return types (never return `None`)
- `AttributeError: 'str' object has no attribute 'get'` when SharePoint returns a string error payload
- Pyright type-checking errors across the library and tests

### Removed
- Python 2.7 support
- `.travis.yml` (use GitHub Actions instead)
- `requirements.txt` / `requirements-dev.txt` (use `uv`/`pyproject.toml`)
- Deprecated/renamed model classes superseded by the regenerated schema

### Internal
- CI moved to GitHub Actions (ruff, pyright, offline pytest)
- Dependency management via `uv` and `pyproject.toml`

---

## [2.6.2]

- Support Access Token Refresh for MSAL-provided tokens ([#953](https://github.com/vgrem/office365-rest-python-client/issues/953))
- Resolved `get_comments()` method issue ([#956](https://github.com/vgrem/office365-rest-python-client/issues/956))
- Added Reply-To and HTML ItemBody type support in `send_mail` ([#958](https://github.com/vgrem/office365-rest-python-client/issues/958))
- Fixed `File.open_binary` issue ([#960](https://github.com/vgrem/office365-rest-python-client/issues/960))
- Fixed linting GitHub Action ([#961](https://github.com/vgrem/office365-rest-python-client/issues/961))

## [2.6.0]

- Support for Azure environments in `ClientContext` (USGovernment, GCC High, etc.)
- Auto-renewal of authentication cookies for `with_user_credentials` (after 30 min expiry) ([#950](https://github.com/vgrem/office365-rest-python-client/issues/950))
- Support for worksheet [used range](https://learn.microsoft.com/en-us/graph/api/worksheet-usedrange) API ([#926](https://github.com/vgrem/office365-rest-python-client/issues/926))

## [2.5.14]

- Added `include_resource_data` to `SubscriptionCollection.add` ([#900](https://github.com/vgrem/office365-rest-python-client/issues/900), [#901](https://github.com/vgrem/office365-rest-python-client/issues/901))
- Added urllib percent-encoding to URLs ([#918](https://github.com/vgrem/office365-rest-python-client/issues/918))
- Microsoft Search API enhancements

## [2.5.13]

- JSON batch request fixes ([#835](https://github.com/vgrem/office365-rest-python-client/issues/835))

## [2.5.12]

- Batch request fixes and improvements ([#788](https://github.com/vgrem/office365-rest-python-client/issues/788))

## [2.5.11]

- Fixed error creating a choice field ([#873](https://github.com/vgrem/office365-rest-python-client/issues/873))
- Fixed `shares.by_url` method ([#872](https://github.com/vgrem/office365-rest-python-client/issues/872))
- Fixed failing driveItem move operation ([#627](https://github.com/vgrem/office365-rest-python-client/issues/627))
- Bumped MSAL dependency ([#869](https://github.com/vgrem/office365-rest-python-client/issues/869))

## [2.5.10]

- Fixed path issue when addressing drive items ([#866](https://github.com/vgrem/office365-rest-python-client/issues/866))

## [2.5.9]

- `DriveItem.get_files` and `get_folders` now retrieve all items beyond default page size ([#844](https://github.com/vgrem/office365-rest-python-client/issues/844))
- Fixed `__str__` raising exception when `DecodeUrl` is `None` ([#850](https://github.com/vgrem/office365-rest-python-client/issues/850))
- Added note for Entra ID permissions when updating SP metadata fields ([#847](https://github.com/vgrem/office365-rest-python-client/issues/847))

## [2.5.8]

- SharePoint resource addressing enhancements
- Introduced methods for granting and revoking delegated & application permissions

## [2.5.7]

- Added passphrase support in `ClientContext.with_client_certificate` ([#836](https://github.com/vgrem/office365-rest-python-client/issues/836))

## [2.5.6]

- Support for folder coloring in SharePoint API ([#693](https://github.com/vgrem/office365-rest-python-client/issues/693))

## [2.5.5]

- Better Range support in OneDrive API ([#745](https://github.com/vgrem/office365-rest-python-client/issues/745))

## [2.5.4]

- SharePoint authentication support for GCC High environments ([#794](https://github.com/vgrem/office365-rest-python-client/issues/794))
- Fixed listing folders instead of files ([#802](https://github.com/vgrem/office365-rest-python-client/issues/802))
- Fixed addressing shared drive items ([#801](https://github.com/vgrem/office365-rest-python-client/issues/801))

## [2.5.3]

- Added `file_name` parameter to `File.copyto` and `File.copyto_using_path` ([#787](https://github.com/vgrem/office365-rest-python-client/issues/787))
- Fixed import error for `TypedDict` on Python 3.7 ([#781](https://github.com/vgrem/office365-rest-python-client/issues/781))
- Fixed `parent_folder` / `parent_collection` empty when retrieving file by server-relative URL ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed 401 on site property update ([#735](https://github.com/vgrem/office365-rest-python-client/issues/735))
- Fixed recipient instance reuse ([#791](https://github.com/vgrem/office365-rest-python-client/issues/791))

## [2.5.2]

- Fixed missing `typing_extensions` dependency on older Python ([#762](https://github.com/vgrem/office365-rest-python-client/issues/762))
- File/folder addressing methods fixes ([#764](https://github.com/vgrem/office365-rest-python-client/issues/764))
- Fixed share file with password ([#766](https://github.com/vgrem/office365-rest-python-client/issues/766))
- Fixed change token entity type name ([#767](https://github.com/vgrem/office365-rest-python-client/issues/767))
- Documentation fixes ([#768](https://github.com/vgrem/office365-rest-python-client/issues/768))
- CI/Linting improvements ([#765](https://github.com/vgrem/office365-rest-python-client/issues/765))

## [2.5.1]

- Added conditional import of `ParamSpec` from `typing_extensions` ([#757](https://github.com/vgrem/office365-rest-python-client/issues/757))

## [2.5.0]

- Introduced `GraphClient.with_client_secret` and `GraphClient.with_username_and_password`
- Fixed `Folder.copy_to_using_path` ([#740](https://github.com/vgrem/office365-rest-python-client/issues/740))
- Fixed `File.download_session` ([#748](https://github.com/vgrem/office365-rest-python-client/issues/748))
- Fixed `ResourcePath` collection ([#744](https://github.com/vgrem/office365-rest-python-client/issues/744))
- Typing improvements (mypy/pyright support) ([#746](https://github.com/vgrem/office365-rest-python-client/issues/746), [#747](https://github.com/vgrem/office365-rest-python-client/issues/747))

## [2.4.4]

- Fixed `FieldCollection.add_dependent_lookup_field` ([#723](https://github.com/vgrem/office365-rest-python-client/issues/723))
- Fixed 404 error with `Web.get_file_by_server_relative_path` ([#722](https://github.com/vgrem/office365-rest-python-client/issues/722))

## [2.4.3]

- Support for interactive auth via `ClientContext.with_interactive`
- Support for OAuth2 device code auth ([#713](https://github.com/vgrem/office365-rest-python-client/issues/713))
- Fixed bug with losing event handlers ([#682](https://github.com/vgrem/office365-rest-python-client/issues/682))

## [2.4.2]

- Fixed error when file is addressed by path ([#645](https://github.com/vgrem/office365-rest-python-client/issues/645))
- File/folder addressing now supports site-relative and web-relative URLs
- Support for long-running actions in Teams API with polling status
