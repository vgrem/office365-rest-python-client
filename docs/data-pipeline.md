# Data pipeline

Move tabular data between Microsoft 365 and the Python data stack (pandas, CSV,
Parquet, SQL, ...). The same surface works on every collection — SharePoint
lists, Entra users/groups, Teams, OneDrive drives — and shares its engine with
the [migration toolkit](https://github.com/vgrem/office365-rest-python-client/tree/master/office365/migration).

## The model

| Object | Meaning | Import | Export |
|---|---|---|---|
| **Collection** (list, users, ...) | a *table* | `from_*` / `queue_*` | `to_*` / `export_to` |
| **File / Folder** | a *blob* (content) | `read_dataframe` | `write_dataframe` |

Two rules keep the names predictable:

- **`from_*` is streaming** (returns an `ImportResult` — bounded, resumable,
  idempotent); **`queue_*` is deferred** queue-all (run with `execute_query()`).
- Collections use `to_*`/`from_*`; files/folders use `read_*`/`write_*` and act on
  a file's **content** (metadata stays as plain properties).

## Vocabulary

Six words carry the pipeline, and each names something the others are not:

| Word | Is | Is not |
|---|---|---|
| **item** | a model instance (`User`, `ListItem`, `DriveItem`) | a dict |
| **row** | cells as a source delivers them (a CSV line, an Excel or DataFrame row), usually text | a typed value |
| **record** | a `dict` keyed by the declared OData names, in declaration order | an item |
| **format** | bytes on a handle: csv, ndjson, json, excel, parquet, orc, feather, sql, dataframe | a record shape |
| **profile** | how the wire spells a value (`JsonProfile`, `as_held()`, `scoped()`) | a format |
| **map** | the caller's batch-at-a-time reshape of records before the type is applied: a column copied, a value computed, a constant, a row dropped or fanned out | the schema — a column's type is `converters` or the declared dtype |

Direction is a separate axis, and the type states it once:

| Question | Answered by |
|---|---|
| What does the type declare? | `schema.columns` |
| May a request serialize this name? | `schema.serializable` yes, `schema.readonly` no |
| Did the caller change it? | the item's changes, set by `set_property()` |
| Must it be sent even when unchanged? | `schema.persistable` — the members a `PATCH` replaces whole (`toRecipients`, `members`, `checklist`) |

A request serializes `serializable ∩ (changed ∪ persistable)` — a delta, not the
*type*. An export carries `columns`, because a read projection has no direction to lose:
`id` and `createdDateTime` are part of what the type is. An import sits between the two
and may only set what a request may carry.

`serialize`/`deserialize` name the *mechanism* — a typed value ↔ its wire spelling — never
a set of names: a `readonly` column is serialized like any other, it is only not sent.

### The conversion layer

A value crosses the wire in one of two directions, and each side has its own verb — they
are not synonyms:

| Verb | Direction | Used by |
|---|---|---|
| `serialize_value` | stored → JSON | `to_json()`, a request body (`build_payload`), a CSV writer |
| `deserialize_value` | raw → declared type | `set_property()`, a response, `deserialize_records` |
| `converter_for` | a `converters=` spec → the callable it names | any `from_*` |
| `parse_*` | one primitive (`parse_date`, `parse_uuid`, ...) | the arms both directions dispatch to |

`converters=` names no direction: it is the *user's* per-column instruction, and
`converter_for` turns one into the single-argument callable that deserializes a cell. A
spec is a callable, a Python type, a type name, or a SharePoint `FieldType` — four
spellings of one callable. A name that is none of them raises, so a typo cannot quietly
mean "no conversion".

One table decides what a type means, and both directions read it: `PRIMITIVES` in
`runtime/odata/edm.py`. A row is *(cell parser, every EDM name)*, so `Edm.Decimal` and
`Decimal` cannot end up with two answers, and `serialize_value`, `deserialize_value`,
`converter_for` and the CSV reader all resolve through that one row. A `str`-declared
column has no parser *by design* — text is the wire spelling already, and a raw `1` must
stay `1`.

Which type a column is declared as is a schema question, answered by
`TypeSchema.of(T).dtypes`; the resolver lives in `runtime/schema.py`, beside the
declarations it reads, and depends on them in one direction only (`value → schema`).

What is left: `time` and `Decimal` have no serializer — `serialize_value` passes them
through, so a payload holding one is refused by `json.dumps` (`Intune`'s
`IosUpdateConfiguration.active_hours_start` is declared `time`). Two lines in
`serialize_value` close it.

## Quick start

```python
import pandas as pd
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
lst = ctx.web.lists.ensure_list("Stocks").execute_query()

# DataFrame -> list (streaming, bounded, resumable, idempotent)
lst.from_dataframe(pd.read_csv("stocks.csv", chunksize=2000), key=["Name", "date"]).execute_batch(concurrency=5)

# list -> DataFrame
df = lst.to_dataframe().execute_query().value
```

## Columns

An export is a projection of the **type**, not of the response: the columns are the
type's declared ones (`TypeSchema.of(T).columns`), in declaration order, spelled the
way the client's service root spells them — so a stable client exports no preview column, and
every format, every page and every run answer the same headers. A name only the page
carries (a SharePoint list item's site columns, which no CSDL describes) follows,
sorted. `.select(...)` replaces that with the names you name — and *adds* to them, so a method
that selects a property it depends on (the identity a filter reads, the child to fan out over)
is not undone by the caller naming its own columns.

```python
lst.to_csv("items.csv").execute_query()  # the type's columns, then the rest
lst.select(["Title", "Modified"]).to_csv("s.csv")  # exactly these two
```

### One row per child

A collection-valued property is a table inside a row, and `rows_from` states it: the property
is added to `$select`, and each child becomes a row whose columns are the child's own fields.

```python
client.users.get_licensed().select(["userPrincipalName"]).get_all().to_csv(
    sys.stdout, rows_from="assignedLicenses"
).execute_query()
# userPrincipalName, skuId, disabledPlans
```

It exists because no projection can name a child: Graph refuses
`$expand=assignedLicenses` ("not a navigation property or complex property") and
`$select=assignedLicenses/skuId` ("Invalid property 'skuId' specified in $select"). Dotted
select fields (`members/displayName`) cover the other case — children the service does
expand — one record per child too, and the two cannot be combined.

A child's columns are the fields its type declares, in declaration order, so a child with an
empty collection writes an empty cell rather than a shorter row. Select at least one column of
the parent, or the rows say nothing about whose they are.

Every exporter takes it — `to_csv`, `to_ndjson`, `to_excel`, `to_parquet`, `to_orc`,
`to_feather`, `to_sql`, `to_duckdb` — and `to_records(rows_from=...)` returns the rows to a
caller instead of writing them.

The import side of the same statement reads those rows back: the format's reader, then
`deserialize_records`, which asks the child's schema what each column means, plus the one
column the child does not declare — its owner — to name the group. `examples/entraid/licenses/import_licences.py`
is that round trip.

A type states its identity above the class — `@key("tenantId")` — and a read always
asks for it even when `.select(...)` omitted it, because that column is what the next
request addresses the item by. Nine Graph types whose key the v1.0 CSDL states as
something other than `id` say so; everything else leaves it at the family default and
behaves as before.

## Formats

`csv`, `tsv`, `json` (array), `ndjson`, `excel`, `parquet`, `orc`, `feather`,
`dataframe` — plus `from_sql`/`to_sql` and `from_duckdb`/`to_duckdb` for
databases. Optional dependencies are extras: `[pandas]`, `[excel]`, `[parquet]`,
`[sql]`, `[duckdb]`.

Every reader/writer accepts a **path**, a `PathLike` or an open **file object**:

```python
lst.from_csv("stocks.csv")  # path
lst.from_csv(open("stocks.csv"))  # file object
lst.to_parquet("stocks.parquet").execute_query()
```

Streaming databases (bounded memory):

```python
lst.from_sql("postgresql://...", query="SELECT * FROM stocks", chunksize=5000).execute_batch(concurrency=5)

lst.from_duckdb(duckdb.connect("analytics.db"), query="SELECT * FROM stocks").execute_batch(concurrency=5)
```

## Idempotency

Pass a natural `key` to make an import duplicate-proof: a SHA-256 hash of the
key column(s) is stored in a `MigrationKey` column (created automatically) and
already-present rows are skipped (`on_conflict="skip"`) or updated
(`on_conflict="update"`). The key is checked on **every** run — fresh or resumed —
so a replayed or overlapping chunk never duplicates.

```python
lst.from_dataframe(df, key=["region", "date"], on_conflict="update").execute_batch()
```

For long runs, add a `checkpoint`: the committed cursor is persisted after each
chunk and a source **signature** (format, chunk size, key columns) is recorded.
If the signature changes between runs, the chunk skip is discarded and the source
is re-scanned — the key keeps it duplicate-free. Checkpoints are written
**atomically** (temp file → `fsync` → rename), so a crash mid-save never leaves a
truncated file that would break the next resume.

The bulk pipeline and the single-entity verb share one `on_conflict` vocabulary
(`"skip"` / `"update"`): to reconcile **one** entity by a natural key, use
`EntityCollection.upsert(key, value, **properties)` (see the
[API reference](api.md#idempotency)).

```python
lst.from_dataframe(
    pd.read_csv("stocks.csv", chunksize=2000),
    key=["Name", "date"],
    checkpoint="stocks.run.json",
    on_error="collect",
    dead_letter="stocks.bad.jsonl",
).execute_batch(concurrency=5)
```

## Typed columns

`List.from_dataframe`/`from_records` provision columns from the dtypes, or from an
explicit `schema={column: FieldType}`. A `FieldType` also drives **value
coercion** (multi-choice, lookup, user, URL, geolocation, ...):

```python
from office365.sharepoint.fields.type import FieldType

lst.from_dataframe(
    df,
    schema={
        "Status": FieldType.Choice,
        "Tags": FieldType.MultiChoice,  # "a; b" or a list
        "Owner": FieldType.User,  # email or {LookupId}
        "Link": FieldType.URL,  # "https://..." or (url, description)
    },
)
```

## Typing a cell

A Graph entity declares its property types, so an import types its cells for free.
Where nothing declares the type — a list item, an undocumented column, a spelling
that differs — pass `converters={column: converter}` to any `from_*`/`queue_records`.
One converter is one callable, spelled four ways:

```python
lst.from_csv(
    "stocks.csv",
    converters={
        "Traded": "Edm.DateTimeOffset",  # a wire type name
        "Price": Decimal,  # a Python type
        "Notes": lambda cell: cell.strip() or None,  # a callable
    },
).execute_batch()

lst.from_dataframe(df, schema={"Tags": FieldType.MultiChoice})  # FieldType is one too
```

Rules worth knowing:

- **A `converters` key is the destination key** — the name `map` left it. A key naming
  a column the type does not declare **raises**, so a typo cannot silently mean "the
  column was dropped". Targets that accept arbitrary columns (list items) are exempt.
- **The converter wins over the declared type**, and runs once. It tolerates an
  already-typed cell (`try_int(30) → 30`), so re-importing typed data is safe.
- **Nothing is guessed.** A column with no `converters` entry and no declared type is
  left exactly as the reader produced it — `30` stays an `int`, `"abc"` stays a
  `str`. `"18/2111"` is a room number, not a date.
- **Per-cell vs per-row.** `converters` types one cell; `map` reshapes the batch
  (one row into several, several into one).

## Reshaping a row

A file's columns are rarely the payload. `map=` is the one reshape step: a function of
`list[dict]` to `list[dict]` that every format hands plain records (never its own chunk),
so it says what the request carries without knowing where the rows came from:

```python
client.users.from_csv(
    "users.csv",
    map=lambda rows: [
        {
            "userPrincipalName": f"{r['userName']}@contoso.com",  # computed
            "mailNickname": r["userName"],
            "accountEnabled": True,  # a constant
            "city": r["city"],  # a source column
            "passwordProfile/password": r["password"],  # a nested path
        }
        for r in rows
    ],
).execute_batch()
```

A key `map` does not build is **not sent** — which is why `userName` above never reaches
the payload — and a column with no declared type and no `converters` entry is left
exactly as the reader produced it. `map` is the escape hatch for *shape*: typing a
column stays with `converters`, which is declarative, so it can also be reused, checked
and applied by a reader that never sees a callable. The two compose: `map` first, then
`converters`, then the declared dtype.

A lambda is never the schema. It cannot travel to the writer, cannot be pushed down into
the reader, and cannot be reused by a migration — which is why the reshape is an option
on the import verb and never the *statement* of the import.

### Two shapes of sink

A file import is the same three stages every time; only the sink differs:

| Stage | Into a collection (rows are items to create) | Into a verb (rows are its arguments) |
|---|---|---|
| read + type | `client.users.from_csv(path)`, `lst.from_csv(path)` | `deserialize_records(AssignedLicense, path, format="csv")` |
| shape, if the row is not the payload | `map=` — one function of records | `{"userPrincipalName": …, "addLicenses": [licence]}` |
| send | `.execute_query()` / `.execute_batch()` | `assign_licences(rows)` + `execute_batch()`, or any verb |

`from_csv` is the packaged form of the first column — reader, type and sink in one call — and it
exists only where the service has a collection that *creates items*. `assignedLicenses` does not:
it is read-only, and `assignLicense` takes the licence list as an argument, so a
`target.from_csv(...)` there would pretend the service has something it does not. The verb is
bulk instead, deferred like every other write:

```python
rows = []
for record in deserialize_records(AssignedLicense, "licences.csv", format="csv", allow_unknown=True):
    upn = record.pop("userPrincipalName")  # the one column the licence does not declare
    rows.append({"userPrincipalName": upn, "addLicenses": [AssignedLicense().hydrate(record)]})
client.users.assign_licences(rows)
client.execute_batch()
```

`userPrincipalName` is the tell: it belongs to the *user*, not to the licence, so the row is a
licence plus its owner — which is why the type cannot be the whole schema here.
`allow_unknown=True` keeps that column, `hydrate` types the rest through the same `set_property`
path a collection sink uses, and the row becomes the verb's own body: the address, plus
`addLicenses` and `removeLicenses` exactly as Graph names them.

`deserialize_records` is what `from_csv` applies too, so a `csv` read yields the same rows whether
or not a collection is attached; the collection verb adds the sink, nothing else.

## Files (document libraries)

```python
folder = ctx.web.lists.get_by_title("Documents").root_folder

# DataFrame -> library file (content)
folder.write_dataframe("stocks.csv", df).execute_query()

# library file -> DataFrame (content)
df = folder.read_dataframe("stocks.csv").execute_query().value
df = file.read_dataframe(format="parquet").execute_query().value

# library file -> list (streaming, idempotent)
lst.from_file("Shared Documents/stocks.csv", key=["Name", "date"]).execute_batch()
```

CSV is written UTF-8 with a BOM so Excel keeps the columns.

## Streaming export

Export a large list without loading it all:

```python
lst.export_to("stocks.csv", page_size=2000).execute_query()  # CSV/TSV/NDJSON/JSON
```

`page_size` streams appendable formats page by page; other formats fall back to a
whole-collection write.

From `async` code the same export is awaitable — each page is fetched and written
on the worker pool, so the event loop stays free ([async guide](async.md#streaming-export)):

```python
await lst.export_to_async("stocks.csv", page_size=2000)
```

## Errors & verification

- `on_error="collect"` records a failing chunk and continues. With a
  `dead_letter` path the chunk is executed record-by-record, so each failing row
  is appended as `{"row", "error", "record"}` for remediation.
- Verify a keyed import against the target:

```python
report = lst.verify(df, key=["Name", "date"])
assert report.ok, report.summary()  # counts + missing keys
```

## Migration parity

The streaming import and the migration toolkit share the engine (`keyed_queue`,
`UpsertTarget`, `Progress`, `OperationStats`) and one `VerificationReport`:

```python
result = lst.from_dataframe(df, key=["id"])
result.run(concurrency=5)  # == execute_batch
report = result.verify(df, key=["id"])
```

### Async

The import terminals gain awaitable twins — the same chunking, checkpointing,
dead-letter and `progress` semantics, only the wait differs:

```python
result = lst.from_dataframe(df, key=["id"])
await result.execute_query_async()  # sequential, awaited
await result.execute_batch_async(concurrency=5)  # server-side batches
await result.run_async(concurrency=5)  # == execute_batch_async
```

`async for chunk in result:` mirrors the sync iteration for callers that drive
execution themselves.
