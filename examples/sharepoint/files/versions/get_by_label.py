"""
Retrieves a specific version of a file by version label.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "SitePages/Home.aspx"
version = ctx.web.get_file_by_server_relative_path(file_url).versions.get_by_label("1.0").execute_query()

print(version)
