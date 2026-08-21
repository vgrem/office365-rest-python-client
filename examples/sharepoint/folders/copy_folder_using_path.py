"""
Demonstrates how to copy a folder using a path.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Copies a folder to a path")
    parser.add_argument("--target-url", default="Shared Documents/Archive/2001/01", help="target folder url")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # creates a temporary folder first in a Documents library
    folder_from = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}")

    # folder_to = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}")
    folder_to_url = args.target_url

    # copies the folder with a new name
    folder = folder_from.copy_to_using_path(folder_to_url).execute_query()
    print(
        "Folder has been copied from '{0}' into '{1}'".format(
            folder_from.server_relative_path, folder.server_relative_path
        )
    )

    # clean up
    folder_from.delete_object().execute_query()
    folder.delete_object().execute_query()


if __name__ == "__main__":
    main()
