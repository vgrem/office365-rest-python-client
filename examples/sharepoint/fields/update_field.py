"""Demonstrates how to update an existing field (title, required, etc.)

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
lib = ctx.web.default_document_library()
field = lib.fields.get_by_internal_name_or_title("Title")
field.set_property("Title", "Document Title")
field.set_property("Required", True)
field.update().execute_query()
print(f"Field updated: {field.internal_name}")
