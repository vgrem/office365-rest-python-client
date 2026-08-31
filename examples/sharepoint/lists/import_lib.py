"""
Import a public GitHub folder tree into a SharePoint document library.

Pulls a real file/folder structure from a public GitHub repository (via the
GitHub API) and uploads it into the library preserving the relative folder
structure — with a tqdm progress bar. Swap ``--source`` for any public
``owner/repo/path``.

Notes:
- The default source is the MDN Web Docs tree (~13k files across ~12k folders);
  ``plotly/datasets`` and ``opencv/opencv/samples/data`` are handy alternatives.
- Enumeration is a single HTTP call (git trees API, ``HEAD`` ref); downloads go
  over plain HTTP from ``raw.githubusercontent.com``.
- ``--limit 0`` (the default) imports every discovered file; cap it with
  ``--limit N`` for a quicker run.
- Files are uploaded with the simple ``upload`` (4MB cap); use
  ``create_upload_session`` for larger files.
- The target library is expected to be fresh: existing folders are not
  overwritten, so re-running against the same library may fail on duplicates.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse
import io

import requests
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.list import List
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


def import_source_file(lib: List, relative_path: str, download_url: str) -> None:
    """Download a public file over HTTP and upload it, preserving its folder path."""
    parts = relative_path.split("/")
    folder = lib.root_folder
    if len(parts) > 1:
        folder = lib.root_folder.folders.ensure_by_path("/".join(parts[:-1])).execute_query()
    folder.files.upload(io.BytesIO(requests.get(download_url).content), parts[-1]).execute_query()


def main():
    parser = argparse.ArgumentParser(description="Import a public GitHub folder into a SharePoint document library")
    parser.add_argument(
        "--source",
        default="mdn/content/files/en-us/web",
        help="public GitHub folder: owner/repo/path",
    )
    parser.add_argument("--limit", type=int, default=10000, help="maximum number of files to import (0 = all)")
    parser.add_argument("--list-title", default="Data_Import", help="target document library title")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    owner, repo, path = args.source.split("/", 2)
    all_files = list_source_files(owner, repo, path)
    source_files = all_files if args.limit == 0 else all_files[: args.limit]
    print(f"Found {len(all_files)} files under {args.source} ({owner}/{repo}) — importing {len(source_files)}")

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    lib = ctx.web.lists.ensure_list(
        title=args.list_title, template_type=ListTemplateType.DocumentLibrary
    ).execute_query()

    for rel_path, download_url in tqdm(source_files, desc="Importing", disable=args.no_progress):
        import_source_file(lib, rel_path, download_url)
    print(f"Imported {len(source_files)} files into '{lib.title}'")


if __name__ == "__main__":
    main()
