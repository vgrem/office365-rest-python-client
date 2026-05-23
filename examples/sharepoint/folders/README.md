# Working with Folders in SharePoint

A **folder** in SharePoint is a container inside a document library.
Every folder has a **server-relative URL** like `/sites/team/Shared Documents/Reports`.
Folders can be nested and each has a unique ID.

This page groups examples by **what you want to do** — not by API endpoint.

---

## ✏️ Create & Set Up

```python
# Create a folder
folder = ctx.web.folders.add("/sites/team/Shared Documents/NewFolder").execute_query()

# Create if it doesn't exist
folder = ctx.web.ensure_folder_path("Shared Documents/Reports").execute_query()

# Create with a color label
colored_folder = ctx.web.folders.add("/sites/team/Shared Docs/Projects", color="Green").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Create a folder** | [`create.py`](./create.py) | By server-relative path |
| **Create if not exists** | [`create_if_not_exist.py`](./create_if_not_exist.py) | No error if already there |
| **Create with color** | [`create_with_color.py`](./create_with_color.py) | Folder coloring in modern UI |
| **Create a document set** | [`create_doc_set.py`](./create_doc_set.py) | A special folder with metadata |

## 🔍 Browse & Discover

```python
# Get a folder by path
folder = ctx.web.get_folder_by_server_relative_url("/sites/team/Shared Docs/Reports").execute_query()

# Check if it exists
exists = ctx.web.get_folder_by_server_relative_url(path).get_exists().execute_query()

# List files inside
files = ctx.web.get_folder_by_server_relative_url(path).files.get().execute_query()

# List subfolders
folders = ctx.web.get_folder_by_server_relative_url(path).folders.get().execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Get folder by path** | [`get_by_path.py`](./get_by_path.py) | By server-relative path |
| **Check if exists** | [`folder_exists.py`](./folder_exists.py) | Returns `True` / `False` |
| **Check if exists (v2)** | [`folder_exists_v2.py`](./folder_exists_v2.py) | Alternative approach |
| **Get by sharing link** | [`get_by_shared_link.py`](./get_by_shared_link.py) | Resolve a sharing link |
| **Get metadata** | [`get_props.py`](./get_props.py) | Name, path, size, item count |
| **Get system metadata** | [`get_system_metadata.py`](./get_system_metadata.py) | Internal SharePoint fields |
| **List files inside** | [`list_files.py`](./list_files.py) | All files in a folder |
| **List subfolders** | [`list_folders.py`](./list_folders.py) | Direct children only |
| **List with custom scope** | [`list_folders_custom.py`](./list_folders_custom.py) | Recursive or filtered |
| **Get files list** | [`get_files.py`](./get_files.py) | Alternative file listing |

## ↔️ Move, Copy & Rename

```python
# Move a folder
folder.move_to("/sites/team/Shared Documents/Archive").execute_query()

# Copy a folder
folder.copy_to("/sites/team/Shared Documents/Backup").execute_query()
```

| What | File | Notes |
|------|------|-------|
| **Move** | [`move.py`](./move.py) | Move to a new location |
| **Move (alternative)** | [`move_alt.py`](./move_alt.py) | Different API endpoint |
| **Copy** | [`copy_folder.py`](./copy_folder.py) | Duplicate with all contents |
| **Copy by path** | [`copy_folder_using_path.py`](./copy_folder_using_path.py) | Uses server-relative path |
| **Rename** | [`rename.py`](./rename.py) | Change the folder name |

## ⬇️ Download

| What | File | Notes |
|------|------|-------|
| **Download as ZIP** | [`download_as_zip.py`](./download_as_zip.py) | Entire folder as a `.zip` |
| **Download files** | [`download.py`](./download.py) | Download files inside |

## 🗑️ Delete

| What | File | Notes |
|------|------|-------|
| **Delete a folder** | [`delete.py`](./delete.py) | Moves to recycle bin |

## 🔗 Share

| What | File | Notes |
|------|------|-------|
| **Share with people** | [`share.py`](./share.py) | Send email with link |
| **Share with external user** | [`share_with_external_user.py`](./share_with_external_user.py) | Guest access |

## ✏️ Update Properties

| File | What it does |
|------|-------------|
| [`set_properties.py`](./set_properties.py) | Change folder metadata fields |

---

## Getting started

```python
from office365.sharepoint.client_context import ClientContext

ctx = ClientContext("https://contoso.sharepoint.com/sites/team").with_client_credentials(
    "your_client_id", "your_client_secret"
)

# Get a folder reference
folder = ctx.web.get_folder_by_server_relative_url("/sites/team/Shared Documents/Reports")
files = folder.files.get().execute_query()
for f in files:
    print(f.name)
```

## Official docs

- [Working with folders — SharePoint REST API](https://learn.microsoft.com/en-us/sharepoint/dev/sp-add-ins/working-with-folders-and-files-with-rest#working-with-folders-by-using-rest)
