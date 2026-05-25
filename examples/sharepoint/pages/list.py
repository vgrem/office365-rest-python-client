"""
List site pages on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_password, test_username
)
site_pages = ctx.site_pages.pages.get().execute_query()
for site_page in site_pages:
    print(site_page)
