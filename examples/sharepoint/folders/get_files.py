"""
Gets files within a folder.

``Folder.get_files()`` pages through the folder, so it also works on folders with
more than the 5,000-item list view threshold (unlike ``ctx.load(folder, ["Files"])``,
which issues a single request and is throttled/trimmed).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Gets files within a folder")
    parser.add_argument("--folder-url", default="Shared Documents", help="folder url")
    parser.add_argument("--recursive", action="store_true", help="include subfolders")
    parser.add_argument("--page-size", type=int, default=2000, help="items per page (keep <= 5000)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant=tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    root_folder = ctx.web.get_folder_by_server_relative_path(args.folder_url)
    files = root_folder.get_files(recursive=args.recursive, page_size=args.page_size).execute_query()
    print(f"Found {len(files)} file(s)")
    for file in files:
        print(file.name)


if __name__ == "__main__":
    main()
