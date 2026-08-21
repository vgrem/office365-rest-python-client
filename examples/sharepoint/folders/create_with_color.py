"""
Demonstrates how to create a folder with a color.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.colors import FolderColors
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Creates a folder with a color")
    parser.add_argument("--name", default="Report1234", help="folder name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

    root_folder = ctx.web.default_document_library().root_folder
    folder = root_folder.folders.add(args.name, color_hex=FolderColors.DarkGreen).execute_query()
    print(f"Folder : {folder.server_relative_url} has been created")


if __name__ == "__main__":
    main()
