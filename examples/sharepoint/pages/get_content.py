"""
Get the canvas and layout web part content of a site page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
page = ctx.site_pages.pages.get_by_name("Home.aspx").execute_query()
print(page.canvas_content)
print(page.layout_web_parts_content)
