"""Demonstrates how to remove a field from a content type.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.contenttypes.creation_information import ContentTypeCreationInformation
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
info = ContentTypeCreationInformation(Name="Project Document", Description="For Contoso projects")
ct = ctx.web.content_types.add(info).execute_query()
field = ctx.web.fields.get_by_internal_name_or_title("Title")
ct.field_links.add(field).execute_query()

# Retrieve the field link and remove it
field_link = ct.field_links.get_by_id(field.id).execute_query()
field_link.delete_object().execute_query()
print(f"Field removed from content type: {field.internal_name}")

# Verify remaining fields
ct_updated = ctx.web.content_types.get_by_id(ct.string_id).execute_query()
remaining = [fl for fl in ct_updated.field_links if fl.field_internal_name != field.internal_name]
print(f"Field links remaining: {len(remaining)}")