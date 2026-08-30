"""
Demonstrates how to delete a folder.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    argparse.ArgumentParser(description="Deletes a folder").parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    folder_name = f"Name{uuid.uuid4().hex[:8]}"  # creates a temporary folder first in Documents library
    folder = ctx.web.default_document_library().root_folder.add(folder_name)
    folder.delete_object().execute_query()
    print("Folder has been deleted")


if __name__ == "__main__":
    main()
