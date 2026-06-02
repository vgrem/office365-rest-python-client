"""Demonstrates how to change the display order of fields in a content type.

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

# Add a few fields
for field_name in ["Title", "Editor", "Author"]:
    field = ctx.web.fields.get_by_internal_name_or_title(field_name)
    ct.field_links.add(field).execute_query()
    print(f"Field added: {field_name}")

# Reorder fields: Author first, then Editor, then Title
ct.reorder_fields(["Author", "Editor", "Title"]).execute_query()
print("Fields reordered: Author → Editor → Title")
