"""
Demonstrates how to rename a page
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

file_url = "Site Pages/Home.aspx"
new_name = "NewHome.aspx"
ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
file = ctx.web.get_file_by_server_relative_path(file_url)
file.rename(new_name).execute_query()
