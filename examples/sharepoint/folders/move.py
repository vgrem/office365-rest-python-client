"""
Demonstrates how to move a folder within a site.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    argparse.ArgumentParser(description="Moves a folder within a site").parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

    print("Creating a temporary folders in a Documents library ...")
    folder_from = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}")
    folder_to_parent = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}")
    # folder_to_url = "Shared Documents/archive"

    print("Moving folder...")
    # folder_to = folder_from.move_to_using_path(folder_to_parent).execute_query()
    folder_to = folder_from.move_to(folder_to_parent).execute_query()
    print("Folder has been moved into '{0}'".format(folder_to.server_relative_url))

    print("Cleaning up temporary folders ...")
    folder_to_parent.delete_object().execute_query()
    print("Done")


if __name__ == "__main__":
    main()
