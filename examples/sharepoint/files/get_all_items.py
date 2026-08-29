"""
Enumerates files and folders within a library
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Enumerate files and folders within the default document library").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    doc_lib = ctx.web.default_document_library()
    items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get_all().execute_query()
    for idx, item in enumerate(items):
        if item.file_system_object_type == FileSystemObjectType.Folder:
            print(f"({idx} of {len(items)})  Folder: {item.folder.server_relative_url}")
        else:
            print(f"({idx} of {len(items)}) File: {item.file.server_relative_url}")


if __name__ == "__main__":
    main()
