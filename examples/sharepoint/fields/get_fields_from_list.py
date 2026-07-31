"""Demonstrates how to retrieve all fields from a SharePoint list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/field
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(
    tenant=tenant,
    client_id=client_id,
    username=username,
    password=password,
)
target_list = ctx.web.lists.get_by_title("Site Pages")
fields = target_list.fields.get().execute_query()
for field in fields:
    print(f"Field name {field.internal_name}")
