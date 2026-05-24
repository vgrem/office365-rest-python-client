"""
Returns a link for downloading the file without authentication.
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "Shared Documents/Financial Sample.xlsx"

result = ctx.web.get_file_by_server_relative_path(file_url).get_pre_authorized_access_url(1).execute_query()
print(result.value)
