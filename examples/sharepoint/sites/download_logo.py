"""
Downloads a site logo to a temporary file.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

client = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = client.site.get_site_logo_ex().execute_query()
download_path = os.path.join(tempfile.mkdtemp(), "SiteLogo.png")
with open(download_path, "wb") as f:
    f.write(result.value)
print("Saved into {0}".format(download_path))
