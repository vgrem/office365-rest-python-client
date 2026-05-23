"""Demonstrates how to create a site field of type Taxonomy (managed metadata)

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
term_set_id = "3b712032-95c4-4bb5-952d-f85ae9288f99"
field = ctx.web.fields.create_taxonomy_field("Country", term_set_id).execute_query()
print(f"Taxonomy field created: {field.internal_name}")
field.delete_object().execute_query()
