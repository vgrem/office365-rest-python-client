"""
Demonstrates how to download a file using a sharing link (guest URL).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

client = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)

sharing_link_url = "https://mediadev8.sharepoint.com/:x:/s/team/EcEbi_M2xQJLng_bvQjPtgoB1rB6BFvMVFixnf4wOxfE5w?e=bzNjb6"

download_path = os.path.join(tempfile.mkdtemp(), "Report.csv")
with open(download_path, "wb") as local_file:
    file = client.web.get_file_by_guest_url(sharing_link_url).download(local_file).execute_query()
print(f"[Ok] file has been downloaded into: {download_path}")
