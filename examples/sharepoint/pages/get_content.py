"""
Get the canvas and layout web part content of a site page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_credentials(test_client_id, test_password, test_tenant, test_username)
page = ctx.site_pages.pages.get_by_name("Home.aspx").execute_query()
print(page.canvas_content)
print(page.layout_web_parts_content)
