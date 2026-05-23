# Working with Files in SharePoint

A file in SharePoint lives inside a **document library** (a special kind of list).
Every file has a **server-relative URL** like `/sites/team/Shared Documents/report.docx`.

This page groups examples by **what you want to do** — not by API endpoint.

---

## ⬆️ Upload

| What | File | Notes |
|------|------|-------|
| **Basic upload** (up to 4 MB) | [`upload.py`](./upload.py) | Simple binary content |
| **Large files** (no size limit) | [`upload_large.py`](./upload_large.py) | Uses `StartUpload` / `ContinueUpload` / `FinishUpload` session |
| CSV (comma-separated) | [`upload_csv.py`](./upload_csv.py) | |
| JSON | [`upload_json.py`](./upload_json.py) | |
| **With checksum verification** | [`upload_with_checksum.py`](./upload_with_checksum.py) | Ensures data integrity |
| **Create Word document** | [`create_word.py`](./create_word.py) | Builds `.docx` from scratch |
| **Create Excel workbook** | [`create_excel.py`](./create_excel.py) | Builds `.xlsx` from scratch |
| **Create wiki page** | [`create_wiki.py`](./create_wiki.py) | Wiki content as a file |

## ⬇️ Download

| What | File | Notes |
|------|------|-------|
| **Basic download** | [`download.py`](./download.py) | Save to local file |
| **Large file download** | [`download_large.py`](./download_large.py) | Streams in chunks |
| **Recent files** | [`download_recent.py`](./download_recent.py) | Last N modified |
| **All files from a library** | [`download_from_lib.py`](./download_from_lib.py) | Bulk download |
| **By URL** | [`download_from_url.py`](./download_from_url.py) | No site context needed |
| **By sharing link** | [`download_by_shared_link.py`](./download_by_shared_link.py) | Anonymous or guest link |
| **Get a download link only** | [`get_download_link.py`](./get_download_link.py) | Returns URL, doesn't download |
| **Version history** | [`versions/list.py`](./versions/list.py) | List all versions |
| **Specific version** | [`versions/get_by_label.py`](./versions/get_by_label.py) | Download by version label |
| **All versions** | [`download_versions.py`](./download_versions.py) | Download every version |

## 🔍 Browse & Discover

| What | File | Notes |
|------|------|-------|
| **List all files** in a library | [`get_all_items.py`](./get_all_items.py) | |
| **Check if a file exists** | [`exists.py`](./exists.py) | Returns `True` / `False` |
| **Get file metadata** | [`get_props.py`](./get_props.py) | Author, created, modified, size |
| **Get extended properties** | [`get_extended_props.py`](./get_extended_props.py) | Custom metadata |
| **Get system metadata** | [`get_system_metadata.py`](./get_system_metadata.py) | Internal SharePoint fields |
| **Get file content as text** | [`get_content.py`](./get_content.py) | Read without saving |
| **Get sharing information** | [`get_sharing_info.py`](./get_sharing_info.py) | Links, permissions, audience |
| **Get checkout status** | [`get_checked_out.py`](./get_checked_out.py) | Is someone editing it? |
| **Get checkout type** | [`get_checkout_type.py`](./get_checkout_type.py) | Online / Offline |
| **By sharing link** | [`get_by_sharing_link.py`](./get_by_sharing_link.py) | Resolve a sharing link to a file |

## ✏️ Edit & Replace

| What | File | Notes |
|------|------|-------|
| **Rename** | [`rename_page.py`](./rename_page.py) | Changes display name |
| **Replace content** | [`replace.py`](./replace.py) | Updates binary while keeping metadata |

## ↔️ Move & Copy

| What | File | Notes |
|------|------|-------|
| **Copy within a site** | [`copy_file.py`](./copy_file.py) | |
| **Copy with new name** | [`copy_file_with_name.py`](./copy_file_with_name.py) | |
| **Copy by server-relative path** | [`copy_using_path.py`](./copy_using_path.py) | Uses path instead of object |
| **Move (rename) within a site** | [`move_file.py`](./move_file.py) | |

## 🗑️ Delete

| What | File | Notes |
|------|------|-------|
| **Delete a file** | [`delete.py`](./delete.py) | Moves to recycle bin |

## 🔗 Share

| What | File | Notes |
|------|------|-------|
| **Share with people** | [`share.py`](./share.py) | Send email with link |
| **Create anonymous link** | [`create_anonymous_link.py`](./create_anonymous_link.py) | "Anyone" link |

## 🔐 Permissions

| File | What it does |
|------|-------------|
| [`permissions/check.py`](./permissions/check.py) | Check if a user has a specific permission |
| [`permissions/list.py`](./permissions/list.py) | List all permissions on a file |
| [`permissions/get.py`](./permissions/get.py) | Get permission details |
| [`permissions/assign.py`](./permissions/assign.py) | Grant or change permissions |

---

## Getting started

All examples use the same pattern:

```python
from office365.sharepoint.client_context import ClientContext
from tests import test_team_site_url, test_client_id, test_client_secret

ctx = ClientContext(test_team_site_url).with_client_credentials(
    test_client_id, test_client_secret
)

# Pick an example and pass `ctx`:
file = ctx.web.get_file_by_server_relative_url("/sites/team/Shared Documents/report.docx")
file.download("report.docx").execute_query()
```

Replace the test imports with your own credentials when running outside the test suite.

## Official docs

- [Working with files — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations)
- [Working with large files by using REST](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest#working-with-large-files-by-using-rest)
