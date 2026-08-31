"""
Export a SharePoint document library's files to a local directory.

Directional migration using the ``SharePointLibrarySource`` adapter: enumerate
the library's files recursively (with progress) and download them preserving the
folder structure. Use ``FileSystemSource`` + ``SharePointLibraryTarget`` to
import back, or point both ends at libraries to migrate library-to-library.

Requires: read access to the library.
"""

import argparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemTarget
from office365.migration.adapters.sharepoint import SharePointLibrarySource
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Export a document library to a local directory")
    parser.add_argument(
        "--library-url",
        required=True,
        help="server-relative library URL, e.g. /sites/project/Shared Documents",
    )
    parser.add_argument("--target", required=True, help="local output directory")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = ctx.web.get_folder_by_server_relative_url(args.library_url)

    job = MigrationJob(SharePointLibrarySource(folder), FileSystemTarget(args.target))
    job.plan()
    stats = job.run()
    print(stats.summary())
    print(job.verify().summary())


if __name__ == "__main__":
    main()
