"""Demonstrates how to upload files into a SharePoint document library

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import argparse
from random import randrange
from typing import Optional

from faker import Faker
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.lists.list import List
from tests.settings import client_id, password, team_site_url, tenant, username


def import_files(target_folder: Folder, files_amount: Optional[int] = None) -> None:
    fake = Faker()
    path = "../../../tests/data/SharePoint User Guide.docx"
    for file_index in range(files_amount or 0):
        file_name = fake.file_name(extension="docx")
        target_file = target_folder.files.upload(path, file_name).execute_query()
        print(f"({file_index} of {files_amount}) File '{target_file.server_relative_url}' has been uploaded")


def import_folders(
    target_lib: List, folders_amount: int, include_files: bool = False, files_amount: Optional[int] = None
) -> None:
    fake = Faker()
    for folder_index in range(folders_amount):
        # 1. Create a folder
        folder_name = fake.date()
        target_folder = target_lib.root_folder.add(folder_name).execute_query()
        print(f"({folder_index} of {folders_amount}) Folder '{target_folder.server_relative_url}' has been created")

        if include_files:
            # 2. Upload a file into a folder
            import_files(target_folder, randrange(0, files_amount))


def main():
    parser = argparse.ArgumentParser(description="Upload files into a SharePoint document library")
    parser.add_argument("--list-title", default="Documents_Archive", help="target document library title")
    parser.add_argument("--files-amount", type=int, default=500, help="number of files to upload")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    lib = ctx.web.lists.get_by_title(args.list_title)
    # import_folders(lib, 1, True, 1000)
    import_files(lib.root_folder, args.files_amount)


if __name__ == "__main__":
    main()
