"""
Demonstrates how to enumerate a folder
"""

from typing import Callable

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from tests import test_client_credentials, test_team_site_url


def enum_folder(parent_folder, action):
    # type: (Folder, Callable[[Folder], None]) -> None
    parent_folder.expand(["Folders"]).get().execute_query()
    action(parent_folder)
    for folder in parent_folder.folders:
        enum_folder(folder, action)


def print_folder_stat(folder):
    # type: (Folder) -> None
    print(folder.server_relative_url)
    print(folder.time_created)


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
root_folder = ctx.web.default_document_library().root_folder
enum_folder(root_folder, print_folder_stat)
