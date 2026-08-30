"""
Demonstrates how to rename a folder.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse
import uuid

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Renames a folder")
    parser.add_argument("--new-name", default="OUT - (Drafts 123)", help="new folder name")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    folder = ctx.web.default_document_library().root_folder.add(f"Name{uuid.uuid4().hex[:8]}")  # create temp folder

    folder.rename(args.new_name).execute_query()

    folder.delete_object().execute_query()


if __name__ == "__main__":
    main()
