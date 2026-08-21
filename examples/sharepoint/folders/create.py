"""
Demonstrates how to create a new folder.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Creates a new folder")
    parser.add_argument("--name", default="Reports", help="folder name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    folder = (
        ctx.web.default_document_library().root_folder.folders.add_using_path(args.name, overwrite=True).execute_query()
    )
    print("Folder : {0} has been created".format(folder.server_relative_url))


if __name__ == "__main__":
    main()
