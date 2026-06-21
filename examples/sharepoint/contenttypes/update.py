"""Demonstrates how to update a content type on a SharePoint site.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, root_site_url, tenant, username

ctx = ClientContext(root_site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)

ct = ctx.web.content_types.get_or_add(name="Order Document", description="For Contoso orders").execute_query()
ct.set_property("Description", "Updated description").update().execute_query()
print(f"Content type updated: {ct.name}")
