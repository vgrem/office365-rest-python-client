"""
Delete a site page by filename.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
page = ctx.site_pages.pages.get_by_name("MyPage.aspx").get().execute_query()
page.delete_object().execute_query()
print("Page deleted: MyPage.aspx")
