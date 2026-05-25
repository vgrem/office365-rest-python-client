"""
Get a site page by its file name.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_tenant, test_username, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_id, test_password, test_tenant, test_username)
site_page = ctx.site_pages.pages.get_by_name("Home.aspx").execute_query()
print(site_page)
