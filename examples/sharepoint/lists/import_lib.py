"""
Import a public GitHub folder tree into a SharePoint document library.

Pulls a real file/folder structure from a public GitHub repository (via the
GitHub API) and uploads it into the library preserving the relative folder
structure, using the library's ``Folder.upload_folder`` (sequential, deferred).

Notes:
- The default source is the MDN Web Docs tree (~13k files across ~12k folders);
  ``plotly/datasets`` and ``opencv/opencv/samples/data`` are handy alternatives.
- Enumeration is a single HTTP call (git trees API, ``HEAD`` ref); downloads go
  over plain HTTP from ``raw.githubusercontent.com``.
- ``--limit 0`` imports every discovered file; cap it with ``--limit N``.
- For parallel transfers use ``MigrationOptions.concurrency`` with the migration
  toolkit's ``MigrationJob`` (see ``examples/sharepoint/migration``).
- The target library is expected to be fresh: existing folders are not
  overwritten, so re-running against the same library may fail on duplicates.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse
import tempfile
from pathlib import Path

import requests
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import client_id, password, team_site_url, tenant, username
from tqdm import tqdm

API = "https://api.github.com"


def list_source_files(owner: str, repo: str, path: str) -> list:
    """List every ``(relative_path, download_url)`` under ``path`` in one HTTP call."""
    tree = requests.get(f"{API}/repos/{owner}/{repo}/git/trees/HEAD?recursive=1").json()["tree"]
    prefix = f"{path}/" if path else ""
    return [
        (e["path"], f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{e['path']}")
        for e in tree
        if e["type"] == "blob" and (not prefix or e["path"].startswith(prefix))
    ]


def download_source_files(source_files: list, dest_dir: Path, no_progress: bool) -> None:
    """Download every source file into ``dest_dir``, preserving its relative path."""
    for relative_path, download_url in tqdm(source_files, desc="Downloading", disable=no_progress):
        target = dest_dir / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(requests.get(download_url).content)


def main():
    parser = argparse.ArgumentParser(description="Import a public GitHub folder into a SharePoint document library")
    parser.add_argument(
        "--source",
        default="mdn/content/files/en-us/web",
        help="public GitHub folder: owner/repo/path",
    )
    parser.add_argument("--limit", type=int, default=50, help="maximum number of files to import (0 = all)")
    parser.add_argument("--list-title", default="Data_Import", help="target document library title")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    owner, repo, path = args.source.split("/", 2)
    all_files = list_source_files(owner, repo, path)
    source_files = all_files if args.limit == 0 else all_files[: args.limit]
    print(f"Found {len(all_files)} files under {args.source} ({owner}/{repo}) — importing {len(source_files)}")

    with tempfile.TemporaryDirectory() as tmp:
        local_dir = Path(tmp)
        download_source_files(source_files, local_dir, args.no_progress)

        ctx = ClientContext(team_site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        lib = ctx.web.lists.ensure_list(
            title=args.list_title, template_type=ListTemplateType.DocumentLibrary
        ).execute_query()

        hook = _progress_hook() if not args.no_progress else None
        lib.root_folder.upload_folder(local_dir, progress=hook).execute_query()

    print(f"Imported {len(source_files)} files into '{lib.title}'")


def _progress_hook():
    from office365.runtime.operations import Progress

    bar = tqdm(desc="Uploading")

    def hook(p: Progress) -> None:
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)

    return hook


if __name__ == "__main__":
    main()
