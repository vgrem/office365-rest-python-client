"""
Create and publish a modern page on a SharePoint site.

https://support.microsoft.com/en-gb/office/create-and-use-modern-pages-on-a-sharepoint-site-b3d46deb-27a6-4b1e-87b8-df851e503dec
https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name, test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
page_title = create_unique_name("Site Page ")
print(f"Creating and publishing a site page: {page_title} ...")
new_page = ctx.site_pages.create_and_publish_page(page_title).execute_query()
print(f"A site page has been created at url: {new_page.absolute_url} ...")
