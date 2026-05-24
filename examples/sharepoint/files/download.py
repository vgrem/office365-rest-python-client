"""
Demonstrates how to download a file from SharePoint site
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
# file_url = "Shared Documents/Sample.pdf"
# file_url = "Shared Documents/big_buck_bunny.mp4"
# file_url = "Shared Documents/Financial Sample.xlsx"
file_url = "Shared Documents/report '123.csv"
download_path = os.path.join(tempfile.mkdtemp(), os.path.basename(file_url))
with open(download_path, "wb") as local_file:
    file = ctx.web.get_file_by_server_relative_path(file_url).download(local_file).execute_query()
    print(f"[Ok] file has been downloaded into: {download_path}")
