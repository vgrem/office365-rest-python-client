"""Demonstrates how to create a site field of type DateTime

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/field
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
field = ctx.web.fields.add_datetime("DueDate").execute_query()
print(f"Date field created: {field.internal_name}")
field.delete_object().execute_query()
