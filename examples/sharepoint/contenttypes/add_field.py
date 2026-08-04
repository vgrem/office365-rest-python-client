"""Demonstrates how to add an existing site column to a content type.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)

ct = ctx.web.content_types.get_or_add(name="Project Document", description="For Contoso projects").execute_query()
field = ctx.web.fields.get_by_internal_name_or_title("Title")
ct.field_links.add(field).execute_query()
print(f"Field added to content type: {field.internal_name}")
