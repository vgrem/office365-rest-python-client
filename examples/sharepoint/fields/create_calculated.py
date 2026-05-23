"""Demonstrates how to create a calculated site field

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
formula = '=CONCATENATE(Author,":",Created)'
field = ctx.web.fields.add_calculated("AuthorCreated", formula).execute_query()
print(f"Calculated field created: {field.internal_name}")
field.delete_object().execute_query()
