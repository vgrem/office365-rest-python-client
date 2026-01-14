""" """

from random import randrange

from faker import Faker

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from office365.sharepoint.lists.list import List
from tests import test_team_site_url, test_user_credentials


def run_files_import(target_folder, files_amount=None):
    # type: (Folder, int) -> None
    fake = Faker()
    path = "../../../tests/data/SharePoint User Guide.docx"
    for file_index in range(files_amount):
        file_name = fake.file_name(extension="docx")
        target_file = target_folder.files.upload(path, file_name).execute_query()
        print(f"({file_index} of {files_amount}) File '{target_file.serverRelativeUrl}' has been uploaded")


def run_folders_import(target_lib, folders_amount, include_files=False, files_amount=None):
    # type: (List, int, bool, int) -> None
    fake = Faker()
    for folder_index in range(folders_amount):
        # 1. Create a folder
        folder_name = fake.date()
        target_folder = target_lib.root_folder.add(folder_name).execute_query()
        print(f"({folder_index} of {folders_amount}) Folder '{target_folder.serverRelativeUrl}' has been created")

        if include_files:
            # 2. Upload a file into a folder
            run_files_import(target_folder, randrange(0, files_amount))


if __name__ == "__main__":
    ctx = ClientContext(test_team_site_url).with_credentials(test_user_credentials)
    lib = ctx.web.lists.get_by_title("Documents_Archive")
    # run_folders_import(lib, 1, True, 1000)
    run_files_import(lib.root_folder, 500)
