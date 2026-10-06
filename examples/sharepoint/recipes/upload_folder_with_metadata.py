"""
Mirror a local folder into a document library, attaching metadata.

Walks a source directory, recreates the folder tree, uploads every file with
``FileCollection.upload_file`` (a simple request below the chunk threshold, a
resumable upload session above it), stamps the list item ``Title`` and any
``--field NAME=VALUE`` metadata, and prints a summary. Re-running skips files
that already exist with the same size and path, so the same command doubles as a
lightweight folder sync.

    python upload_folder_with_metadata.py --source ./reports --library "Project Files"
    python upload_folder_with_metadata.py --source ./reports --field ProjectStage=Review --dry-run

Requires ``Sites.ReadWrite.All`` or an owner-level account on the target site.
Metadata fields must already exist on the library (see
``provision_project_workspace.py``).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from __future__ import annotations

import argparse
from pathlib import Path

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

DEFAULT_CHUNK_SIZE = 10 * 1024 * 1024  # 10 MB: threshold and session chunk size


def parse_field(value: str) -> tuple[str, str]:
    """Parse a ``NAME=VALUE`` metadata pair for ``--field``."""
    name, sep, val = value.partition("=")
    if not sep or not name.strip():
        raise argparse.ArgumentTypeError(f"expected NAME=VALUE, got {value!r}")
    return name.strip(), val.strip()


def index_remote(folder, prefix: str = "") -> dict[str, int]:
    """Map every file under ``folder`` to its size, walking subfolders."""
    index = {}
    for f in folder.files.get().execute_query():
        index[f"{prefix}/{f.name}".lstrip("/")] = f.length or 0
    for sub in folder.folders.get().execute_query():
        index.update(index_remote(sub, f"{prefix}/{sub.name}".lstrip("/")))
    return index


def main() -> None:
    parser = argparse.ArgumentParser(description="Mirror a local folder into a document library with metadata")
    parser.add_argument("--source", required=True, help="local folder to upload")
    parser.add_argument("--library", default="Project Files", help="target document library title")
    parser.add_argument(
        "--field",
        action="append",
        default=[],
        type=parse_field,
        metavar="NAME=VALUE",
        help="metadata field to set on every uploaded item (repeatable)",
    )
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="upload-session chunk size in bytes")
    parser.add_argument("--dry-run", action="store_true", help="show what would be uploaded, then exit")
    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.is_dir():
        parser.error(f"source is not a folder: {source}")
    local_files = sorted(p for p in source.rglob("*") if p.is_file())
    if not local_files:
        print(f"No files found under {source}")
        return

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    library = ctx.web.lists.get_by_title(args.library).get().execute_query()
    root = library.root_folder

    remote = {} if args.dry_run else index_remote(root)

    uploaded = skipped = 0
    total_bytes = 0
    for path in local_files:
        rel = path.relative_to(source).as_posix()
        size = path.stat().st_size
        if remote.get(rel) == size:
            skipped += 1
            print(f"  skip  {rel} ({size:,} bytes, unchanged)")
            continue
        if args.dry_run:
            uploaded += 1
            total_bytes += size
            print(f"  plan  {rel} ({size:,} bytes)")
            continue

        parent_rel = Path(rel).parent.as_posix()
        target = root if parent_rel == "." else root.ensure_folder(parent_rel)
        file = target.files.upload_file(path, chunk_size=args.chunk_size).execute_query()

        item = file.listItemAllFields
        item.set_property("Title", path.stem)
        for name, value in args.field:
            item.set_property(name, value)
        item.update().execute_query()

        uploaded += 1
        total_bytes += size
        print(f"  up    {rel} ({size:,} bytes)")

    verb = "Planned" if args.dry_run else "Uploaded"
    print(f"\n{verb}: {uploaded} file(s), skipped: {skipped}, bytes: {total_bytes:,}")


if __name__ == "__main__":
    main()
