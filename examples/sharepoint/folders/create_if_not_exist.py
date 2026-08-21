"""
Returns a folder from a given site-relative path, creating it if it does not exist.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Returns a folder, creating it if it does not exist")
    parser.add_argument("--folder-url", default="Shared Documents/Archive/2023/10/1", help="site-relative folder path")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = ctx.web.ensure_folder_path(args.folder_url).get().select(["ServerRelativePath"]).execute_query()
    print(folder.server_relative_path)


if __name__ == "__main__":
    main()
