"""
Demonstrates how to move a folder within a site using MoveCopyUtil.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.utilities.move_copy_options import MoveCopyOptions
from office365.sharepoint.utilities.move_copy_util import MoveCopyUtil
from tests.settings import client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Moves a folder using MoveCopyUtil")
    parser.add_argument("--path", default="../../data/report.csv", help="file to upload")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

    print("Creating a temporary folders in a Documents library ...")
    folder_from = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}").execute_query()
    folder_from.files.upload(args.path).execute_query()
    folder_to_url = "Shared Documents/{0}".format(f"Name{uuid.uuid4().hex[:8]}")

    print("Moving folder...")
    opt = MoveCopyOptions()
    MoveCopyUtil.move_folder(ctx, folder_from.server_relative_url, folder_to_url, opt).execute_query()
    print("Folder has been moved into '{0}'".format(folder_to_url))

    print("Cleaning up temporary resources ...")
    folder_to = ctx.web.get_folder_by_server_relative_url(folder_to_url)
    folder_to.delete_object().execute_query()
    print("Done")


if __name__ == "__main__":
    main()
