"""
Demonstrates how to retrieve folders.
If the 'recursive' flag is set to True, it traverses all sub folders.

The ``progress`` hook fires once per scanned folder — each folder is printed as
it is discovered via ``items``.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.folders.folder import Folder
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def print_folders(p: Progress[Folder]) -> None:
    """Fired per scanned folder — print each folder discovered in that folder."""
    for folder in p.items or []:
        print(f"Url: {folder.server_relative_url}, Created: {folder.time_created}")


def main():
    parser = argparse.ArgumentParser(description="Gets the folders from a folder")
    parser.add_argument("--recursive", action="store_true", help="traverse all sub folders")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    root = ctx.web.default_document_library().root_folder
    root.get_folders(args.recursive, progress=print_folders).execute_query()


if __name__ == "__main__":
    main()
