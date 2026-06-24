"""
Create a modern page on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name
from tests.settings import client_id, client_secret, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
page_title = create_unique_name("Site Page ")
draft_page = ctx.site_pages.create_page(page_title).execute_query()
print(f"Page created: {draft_page.absolute_url}")
