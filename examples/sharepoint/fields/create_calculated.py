"""Demonstrates how to create a calculated site field

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
formula = '=CONCATENATE(Author,":",Created)'
field = ctx.web.fields.add_calculated("AuthorCreated", formula).execute_query()
print(f"Calculated field created: {field.internal_name}")
field.delete_object().execute_query()
