"""
Create and publish a modern page on a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import create_unique_name
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

page_title = create_unique_name("Site Page ")
new_page = ctx.site_pages.create_and_publish_page(page_title).execute_query()
print(f"Published page: {new_page.absolute_url}")
