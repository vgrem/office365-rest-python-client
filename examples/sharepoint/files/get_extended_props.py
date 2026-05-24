"""
Retrieves file extended properties (accessible via associated ListItem)
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
file_url = "SitePages/Home.aspx"
file_item = ctx.web.get_file_by_server_relative_url(file_url).listItemAllFields.get().execute_query()
for k, v in file_item.properties.items():
    print(f"{k}: {v}")
