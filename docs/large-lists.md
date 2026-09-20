# Large lists and folders

SharePoint enforces a **list view threshold** (5,000 items by default). Queries
that filter or sort on a **non-indexed** column and would scan/return more than
the threshold are blocked with `SPQueryThrottledException` (HTTP 500), and some
single-shot collection loads are silently **trimmed** to 5,000 rows. This page
shows how to avoid and diagnose it.

## Symptoms

- `SPQueryThrottledException: The attempted operation is prohibited because it exceeds the list view threshold.`
- A folder/list query returns exactly 5,000 rows.
- A warning like *"returned 5,000 items in a single request and may be truncated …"*.
- Uploading into a very large document library fails with the same error.

The library classifies this error as
`office365.sharepoint.exceptions.SPQueryThrottledException`, and its message
appends concrete guidance. Classification keys off the **language-independent
error code**, so localized messages still match.

## Fix 1 — page through the data

Use the paged entry points instead of a single-shot load, and keep `page_size`
at or below the threshold:

```python
# list items (server-driven $skiptoken paging)
items = lst.items.get_all(page_size=2000).execute_query()

# a folder's files — pages automatically, so >5,000-item folders work
files = folder.get_files(page_size=2000).execute_query()          # recursive=True to descend

# CAML query — iterating continues from the last item (ListItemCollectionPosition)
for item in lst.get_items(query, page_size=2000).execute_query():
    ...
```

> `ctx.load(folder, ["Files"])` and `lst.get_items(query)` (without `page_size`)
> issue a **single** request and can be throttled/trimmed on large collections.
> `folder.files` / `folder.folders` / `list.items` are also read single-shot when
> loaded via `ctx.load(...)`.
>
> The library warns when such a load reaches the threshold — the collection is
> list-view-backed, so it is *hinted* rather than silently truncated. `get_all` /
> `get_files` / `get_items(..., page_size=...)` never warn.

## Fix 2 — index the filtered/sorted column

Indexing a column lets queries filter and sort past the threshold. The column
must already exist:

```python
lst.ensure_indexed("Status").execute_query()
```

`ID` is always indexed, so `ID > 0` is a safe broad filter. Indexing is a schema
change and is **never done implicitly** — call `ensure_indexed` yourself. Note
that SharePoint builds the index **in the background** (seconds to minutes for a
large list), so a query issued immediately after may still be throttled; re-run
once the build finishes.

To see which columns a query would need indexed:

```python
lst.index_candidates(query)   # -> ['Status', 'date']  (query.index_candidates)
```

## Fix 3 — filter on an indexed column

```python
lst.items.filter("ID gt 0").get_all(page_size=2000).execute_query()
```

## Pre-flight a CAML query

`List.check_query` verifies the query before sending it, and raises
`SPQueryThrottledException` **naming the columns to index** instead of letting the
server return an opaque 500 (it performs 1–2 requests):

```python
lst.check_query(query)                              # explicit
lst.get_items(query, page_size=2000, check=True)    # or pre-flight inside get_items
```

`check=False` (the default) keeps `get_items` deferred with no extra request.

## Diagnosing

- `lst.ensure_property("ItemCount").execute_query()` then `lst.item_count`.
- `lst.index_candidates(query)` — the columns to index for a query.
- List settings → **Indexed columns** (add indexes there, or with `ensure_indexed`).
- If `List.get_items` warns *"not paged"*, pass `page_size=`.
- A truncation warning means the collection hit the threshold in one request —
  switch to `get_all` / `get_files` / `get_items(..., page_size=...)`.

## Uploading into a very large library

`Folder.upload_file(...)` — and the first step of `FileCollection.create_upload_session`
— use the `Files/add` endpoint, which SharePoint implements with an internal
query. On a library above the threshold this can return `SPQueryThrottledException`
**even though you are only writing**, and there is no SharePoint REST upload
endpoint that avoids it. Workarounds:

- upload via **Microsoft Graph** (`DriveItem` upload session — see
  `examples/onedrive/files/upload_large.py`);
- upload into a subfolder whose item count is under the threshold; or
- reduce the library size (move/archive old items).

The library surfaces this as `SPQueryThrottledException` with guidance so it is
clear the cause is the threshold, not the upload itself.

## Notes

- Lists allow roughly 20 indexed columns; indexed text columns are limited to 255
  characters — `ensure_indexed` surfaces the server error if the limit is hit.
- Sorting on a non-indexed column is the most reliable trigger: SharePoint can
  trim a plain filter to 5,000, but it cannot trim a full sort.
- See `examples/sharepoint/lists/query_large_list.py` (paged CAML),
  `examples/sharepoint/folders/get_files.py` (paged folder files) and
  `examples/sharepoint/files/list_large_folder.py` (recursive folder scan).
