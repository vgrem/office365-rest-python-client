"""
Promote or demote a page as news on the SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
page = ctx.site_pages.pages.get_by_name("MyPage.aspx").get().execute_query()
page.promote_to_news().execute_query()
print("Page promoted to news: MyPage.aspx")
