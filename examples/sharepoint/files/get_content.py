"""
Demonstrates how to download file content.
Intended for small files (with a size less than 4 MB).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file = ctx.web.lists.get_by_title("Site Pages").root_folder.files.get_by_url("Home.aspx")
file_content = file.get_content().execute_query()
print("[Ok] file content has been downloaded")
