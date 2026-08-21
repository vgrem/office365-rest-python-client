"""
Retrieves collection of checked-out files in a document library
"""

import argparse
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    argparse.ArgumentParser(description="Retrieve checked-out files in the default document library").parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    doc_lib = ctx.web.default_document_library()

    files = doc_lib.items.top(1).get().execute_query()
    if len(files) < 1:
        sys.exit("No files were found")

    items = doc_lib.get_checked_out_files().execute_query()
    if len(items) == 0:
        sys.exit("No files were checked out")


if __name__ == "__main__":
    main()
