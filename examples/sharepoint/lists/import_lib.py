"""
Import a public GitHub folder tree into a SharePoint document library.

Pulls a real file/folder structure from a public GitHub repository (via the
GitHub API) and uploads it into the library preserving the relative folder
structure — with a tqdm progress bar. Swap ``--source`` for any public
``owner/repo/path``.

Notes:
- ``upload`` supports files up to 4MB; use ``create_upload_session`` for larger.
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


def default_branch(owner: str, repo: str) -> str:
    """Resolve the repository's default branch name."""
    data = requests.get(f"{API}/repos/{owner}/{repo}").json()
    return data.get("default_branch", "master")


def list_source_files(owner: str, repo: str, branch: str, path: str) -> list:
    """Recursively list ``(relative_path, download_url)`` for every file under ``path``.

    Subdirectories are visited first so nested files (and thus folder creation)
    appear early in the result.
    """
    files: list = []

    def _walk(current: str) -> None:
        entries = requests.get(f"{API}/repos/{owner}/{repo}/contents/{current}?ref={branch}").json()
        if not isinstance(entries, list):
            raise RuntimeError(f"Failed to list GitHub folder '{current}': {entries}")
        entries.sort(key=lambda entry: (entry["type"] == "file", entry["path"]))
        for entry in entries:
            if entry["type"] == "dir":
                _walk(entry["path"])
            elif entry["type"] == "file":
                files.append((entry["path"], entry["download_url"]))

    _walk(path)
    return files


def import_source_file(lib: List, relative_path: str, download_url: str) -> None:
    """Download a public file and upload it, preserving its folder path."""
    parts = relative_path.split("/")
    content = requests.get(download_url).content
    folder = lib.root_folder
    if len(parts) > 1:
        folder = lib.root_folder.folders.ensure_by_path("/".join(parts[:-1])).execute_query()
    folder.files.upload(io.BytesIO(content), parts[-1]).execute_query()


def main():
    parser = argparse.ArgumentParser(description="Import a public GitHub folder into a SharePoint document library")
    parser.add_argument("--source", default="opencv/opencv/samples/data", help="public GitHub folder: owner/repo/path")
    parser.add_argument("--limit", type=int, default=100, help="maximum number of files to import")
    parser.add_argument("--list-title", default="OpenCV", help="target document library title")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    owner, repo, path = args.source.split("/", 2)
    branch = default_branch(owner, repo)
    source_files = list_source_files(owner, repo, branch, path)[: args.limit]
    print(f"Found {len(source_files)} files under {args.source} ({owner}/{repo}@{branch})")

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
