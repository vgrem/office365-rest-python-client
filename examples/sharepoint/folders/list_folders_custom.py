"""
Demonstrates how to enumerate folders recursively using a custom callback.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
from typing import Callable

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def enum_folder(parent_folder: Folder, action: Callable[[Folder], None]) -> None:
    parent_folder.expand(["Folders"]).get().execute_query()
    action(parent_folder)
    for folder in parent_folder.folders:
        enum_folder(folder, action)


def print_folder_stat(folder: Folder) -> None:
    print(folder.server_relative_url)
    print(folder.time_created)


def main():
    argparse.ArgumentParser(description="Enumerates folders recursively").parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    root_folder = ctx.web.default_document_library().root_folder
    enum_folder(root_folder, print_folder_stat)


if __name__ == "__main__":
    main()
