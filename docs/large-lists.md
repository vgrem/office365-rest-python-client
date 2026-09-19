# Large lists and folders

SharePoint enforces a **list view threshold** (5,000 items by default). Queries
that filter or sort on a **non-indexed** column and would scan/return more than
the threshold are blocked with `SPQueryThrottledException` (HTTP 500), and some
single-shot collection loads are silently **trimmed** to 5,000 rows. This page
shows how to avoid and diagnose it.

## Symptoms

- `SPQueryThrottledException: The attempted operation is prohibited because it exceeds the list view threshold.`
- A folder/list query returns exactly 5,000 rows.
- Uploading into a very large document library fails with the same error.

The library classifies this error as
`office365.sharepoint.exceptions.SPQueryThrottledException`, and its message
appends concrete guidance. Classification keys off the **language-independent
error code**, so localized messages still match.

## Fix 1 — page through the data

Use `get_all` (server-driven paging) instead of a single-shot load, and keep
`page_size` at or below the threshold:

```python
# list items
items = lst.items.get_all(page_size=2000).execute_query()

# a folder's files — pages automatically, so >5,000-item folders work
files = folder.get_files(page_size=2000).execute_query()

# CAML query — iterating follows the server __next link
for item in lst.get_items(query, page_size=2000).execute_query():
    ...
```

> `ctx.load(folder.files)` and `lst.get_items(query)` (without `page_size`) issue a
> **single** request and can be throttled/trimmed on large collections. Prefer
> `get_all(...)` / `get_items(..., page_size=...)`.

## Fix 2 — index the filtered/sorted column

Indexing a column lets queries filter and sort past the threshold:

```python
lst.ensure_indexed("Status").execute_query()
```

`ID` is always indexed, so `ID > 0` is a safe broad filter. Indexing is a schema
change and is **never done implicitly** — call `ensure_indexed` yourself.

## Fix 3 — filter on an indexed column

```python
lst.items.filter("ID gt 0").get_all(page_size=2000).execute_query()
```

## Diagnosing

- `lst.ensure_property("ItemCount").execute_query()` then `lst.item_count`.
- List settings → **Indexed columns** (add indexes there, or with `ensure_indexed`).
- If `List.get_items` warns *"not paged"*, pass `page_size=`.

## Notes

- Lists allow roughly 20 indexed columns; indexed text columns are limited to 255
  characters — `ensure_indexed` surfaces the server error if the limit is hit.
- Sorting on a non-indexed column is the most reliable trigger: SharePoint can
  trim a plain filter to 5,000, but it cannot trim a full sort.
- Run `examples/sharepoint/lists/query_large_list.py --reproduce` to see the error,
  and `examples/sharepoint/files/list_large_folder.py` for the paged alternative.
