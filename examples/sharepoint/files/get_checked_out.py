"""
Retrieves collection of checked-out files in a document library
"""

import sys

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
doc_lib = ctx.web.default_document_library()

files = doc_lib.items.top(1).get().execute_query()
if len(files) < 1:
    sys.exit("No files were found")


items = doc_lib.get_checked_out_files().execute_query()
if len(items) == 0:
    sys.exit("No files were checked out")
