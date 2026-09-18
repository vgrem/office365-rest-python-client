# API Reference

A practical tour of what the library gives you: the two clients, authentication,
the query patterns that make it ergonomic, and the power-user features
(proxy, custom SSL, timeouts, concurrent batching, CSV export, throttling).

## The two clients

| | `ClientContext` | `GraphClient` |
|---|---|---|
| **Target API** | SharePoint REST API v1 | Microsoft Graph API |
| **Use for** | SharePoint lists, files, folders, search, site admin, permissions | Outlook, OneDrive, Teams, OneNote, Planner, Users, Groups |

```python
from office365.graph_client import GraphClient
from office365.sharepoint.client_context import ClientContext

graph = GraphClient(tenant="contoso.onmicrosoft.com").with_client_secret("client_id", "client_secret")

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_secret(
    "contoso.onmicrosoft.com", "client_id", "client_secret"
)
```

## Authentication

Every modern flow is built in — client secret, certificate, username/password,
device code, and interactive (plus on-prem NTLM and cookies for SharePoint):

| Flow | `GraphClient` | `ClientContext` |
|---|---|---|
| Client secret | `with_client_secret(client_id, secret)` | `with_client_secret(tenant, client_id, secret)` |
| Certificate | `with_certificate(client_id, thumbprint, key)` | `with_client_certificate(tenant, client_id, thumbprint, cert_path)` |
| Username / password | `with_username_and_password(client_id, user, password)` | `with_username_and_password(tenant, client_id, user, password)` |
| Device code | `with_device_flow(client_id)` | `with_device_flow(tenant, client_id, scopes)` |
| Interactive | `with_token_interactive(client_id)` | `with_interactive(tenant, client_id, scopes)` |
| On-prem (NTLM) | — | `with_user_credentials(username, password)` |
| Cookies / custom | `with_token_callback(...)` | `with_cookies(...)`, `with_access_token(...)` |

See [the auth examples](auth/index.md) for full, runnable flows.

## Query patterns

### Filtering

OData `$filter` works identically on both clients:

```python
guests = client.users.filter("userType eq 'Guest'").get().execute_query()
files = ctx.web.lists.get_by_title("Documents").items.filter("FSObjType eq 0").get().execute_query()
```

For complex SharePoint queries, use a CAML query instead:

```python
from office365.sharepoint.listitems.caml.query import CamlQuery

qry = CamlQuery()
qry.ViewXml = "<View><Query><Where><Eq><FieldRef Name='Status'/><Value Type='Text'>Active</Value></Eq></Where></Query></View>"
items = ctx.web.lists.get_by_title("Tasks").get_items(qry).execute_query()
```

### Paging

`get_all()` follows server-driven paging (`@odata.nextLink`) so you never write
paging code:

```python
for user in client.users.get_all().execute_query():
    print(user.user_principal_name)
```

SharePoint collections expose `paged(page_size, page_loaded)` and
`get_all(page_size, page_loaded)`:

```python
all_items = ctx.web.lists.get_by_title("Contacts_Large").items.get_all(500).execute_query()
```

### Batching

Queue operations and submit them as a single OData `$batch` request — and run
several batches concurrently to cut wall time on large imports:

```python
target_list = ctx.web.lists.get_by_title("Documents")
for i in range(100):
    target_list.add_item({"Title": f"Item {i}"})
ctx.execute_batch(items_per_batch=100)      # one $batch request
ctx.execute_batch(concurrency=5)            # 5 batches in flight, retries on 429
```

### Throttling & retries

`execute_query_retry()` retries when Microsoft 365 throttles your request:

```python
result = client.users.top(10).get().execute_query_retry()
```

## Power features

### Proxy, custom SSL, timeouts

Configure the transport once — every request (including internal ones like the
form digest) inherits it:

```python
ctx = (
    ClientContext("https://contoso.sharepoint.com/sites/team")
    .with_client_certificate("tenant", "client_id", "thumbprint")
    .with_transport(
        proxies={"https": "http://proxy:8080"},
        verify="/path/to/ca-bundle.pem",   # or False for testing only
        timeout=30,
    )
)
```

> For MSAL authentication traffic to `login.microsoftonline.com`, set the
> `HTTPS_PROXY` environment variable instead — MSAL reads it directly.

### CSV export

Collections export straight to CSV (or a pandas DataFrame with the `pandas`
extra):

```python
with open("users.csv", "w", newline="") as f:
    client.users.get_all().select(["displayName", "userPrincipalName"]).to_csv(f).execute_query()
```

### DataFrame import / bulk load

Every collection exposes the same adapters over one shared projection: export via
`to_records()`/`to_dataframe()`/`to_csv()`/`to_ndjson()`/`to_excel()` (or the
generic `export_to(..., format=...)`, e.g. `format="json"`), and import via the
**streaming** `from_*` family (`from_records`, `from_dataframe`, `from_csv`,
`from_json`, `from_ndjson`, `from_excel`, …).

The naming is consistent: **`from_*` returns a streaming `ImportResult`** (bounded,
resumable, idempotent); **`queue_*`** (`queue_records`/`queue_dataframe`) is the
deferred queue-all path (run with `execute_query()`).

`List.from_dataframe()` provisions the typed columns once (inferred from the
dtypes, or from an explicit `schema`), then queues, executes, and discards each
chunk — so memory stays bounded no matter the row count. Pick the execution
terminal — the driver itself carries no execution knobs:

```python
import pandas as pd

lst = ctx.web.lists.ensure_list("Housing").execute_query()

lst.from_dataframe(df).execute_query()                            # sequential
lst.from_dataframe(pd.read_csv("housing.csv", chunksize=2000)) \
   .execute_batch(items_per_batch=100, concurrency=5)             # batched
```

For full control, iterate the driver and drive execution yourself:

```python
for _ in lst.from_dataframe(pd.read_csv("housing.csv", chunksize=2000)):
    ctx.execute_batch(items_per_batch=100, concurrency=5)
```

`concurrency>1` runs batches in parallel with per-sub-request throttling retries
(honoring `Retry-After`).

For **long-running** jobs, pass a `checkpoint`: the committed cursor is persisted
atomically after each chunk, so an interrupted run resumes by skipping the
already-committed chunks (progress continues from that offset). `on_error="collect"`
records a failing chunk (in `ImportStats.errors` and the checkpoint's `failures`)
and continues instead of aborting:

```python
lst.from_dataframe(pd.read_csv("housing.csv", chunksize=2000),
                   checkpoint="housing.run.json",
                   on_error="collect") \
   .execute_batch(items_per_batch=100, concurrency=5)
```

`checkpoint` accepts a path (`FileCheckpointStore`), an `ImportCheckpoint` or
`None` (`MemoryCheckpointStore`), or any `CheckpointStore` — pluggable
persistence, MSAL-cache style. The driver exposes `ImportResult.resumed_from`
(rows already committed) and `ImportResult.checkpoint` (live cursor), and
`ImportStats.resumed_from` / `stats.summary()` report the resumed offset.

The generic entry point is `collection.from_records(batches)` for any
`ClientObjectCollection`. See `examples/sharepoint/lists/from_dataframe.py`
and `from_dataframe_large.py`, and the `examples/entraid` DataFrame export for
the Graph side.

#### Idempotent imports (skip / upsert)

Pass a natural `key` (one or more columns) to make the import **duplicate-proof**:
a SHA-256 hash of those columns is stored in `key_field` (created if missing),
the existing keys are loaded once, and a re-run either skips already-present
rows (`on_conflict="skip"`) or updates them (`on_conflict="upsert"`):

```python
lst.from_dataframe(pd.read_csv("housing.csv", chunksize=2000),
                   key=["region", "date"],           # natural key -> MigrationKey hash
                   on_conflict="upsert") \
   .execute_batch(items_per_batch=100, concurrency=5)
```

This works alongside `checkpoint` (resume) — the checkpoint skips committed
chunks for speed, and the key makes the import idempotent on a fresh run, on a
resumed run, and when a chunk is replayed. The existing keys are loaded once per
run (fresh **or** resumed; key values + `Id` only, paged). The checkpoint stores
a source signature (format, chunk size, key columns): if it changes between runs
(e.g. a different `chunksize`), the chunk skip is discarded and the source is
re-scanned — the key keeps it duplicate-free.

Pass `enforce_unique=True` to mark the key column unique on the list (guards
against a create race), and `dry_run=True` to preview the create/update/skip plan
without writing anything.

The import/export surface lives on `RecordCollection` (the base of every typed
`EntityCollection`), so the same API works on any collection. `List` mirrors it as
a facade: `List.from_dataframe`/`from_records`/`from_file` (streaming),
`List.queue_dataframe`/`queue_records` (deferred), `List.export_to`/`to_dataframe`
(record export), and `List.export` (a `.zip` **package** export — per-item JSON +
optional content — distinct from the record export):

```python
collection.export_to(f, format="csv").execute_query()        # unified record export
collection.from_dataframe(df, key=["id"], on_conflict="upsert")  # unified streaming import
collection.from_records(batches, checkpoint="run.json")      # stream record batches

lst.queue_dataframe(df).execute_query()                      # deferred (queue-all)
lst.export_to(f, format="csv").execute_query()               # list -> records
lst.export(zip_file, include_content=True).execute_query()   # list -> .zip package
```

The format registry (`office365.runtime.converters.registry`) maps a format name
to its reader/writer, so adding a format is a registration — the named
`to_csv`/`from_dataframe` conveniences are thin wrappers over it. Built-in
formats: `csv`, `tsv`, `json`, `ndjson`, `excel`, `parquet`, `orc`, `feather`,
`dataframe`; databases stream through `from_sql`/`from_duckdb` (and `to_sql`/
`to_duckdb`). Optional dependencies are extras: `[pandas]`, `[excel]`,
`[parquet]`, `[sql]`, `[duckdb]`. Readers and writers accept a path, a
`PathLike` or an open file object.

### Idempotency

Two idempotent layers, one model — a re-run never duplicates:

- **Metadata (`ensure_*`)** — get-or-create a resource (field, list, content type,
  term, folder, user …), deferred; run with `execute_query()`. Pass
  `on_conflict="update"` to **reconcile** an existing definition (the metadata
  analogue of upsert):

  ```python
  lst.ensure_field("Status", FieldType.Text).execute_query()                 # create if missing
  lst.ensure_fields({"Region": FieldType.Text, "Amount": FieldType.Number})   # -> list[Field]
  lst.ensure_field("Status", FieldType.Choice, on_conflict="update")          # reconcile
  ```

  All client-side `ensure_*` share the `office365.runtime.queries.get_or_create`
  primitives (`get_or_create`/`create_or_get`), so error classification and the
  deferred queueing behave the same everywhere. (Some `ensure_*` — e.g.
  `ensure_site_pages_library`, `ensure_user` — are server-side operations and are
  already idempotent.)

- **Data (`from_records(key=…, on_conflict=…)`)** — get-or-create/update records
  by a natural key (see *Idempotent imports* above).

Distinct from both: `ClientObject.ensure_property`/`ensure_properties` is a
*client-side lazy load* (fetch a property if not already loaded), not a
server-side get-or-create.

## Learn more

-   **[Products](products/index.md)** — start with the SharePoint area, then
    browse the rest from the left navigation.
-   **[Auth examples](auth/index.md)** — all authentication flows.
-   **[README](https://github.com/vgrem/office365-rest-python-client#readme)** —
    installation, the full auth matrix, and per-service guides.
