"""Basic end-to-end content type usage.

Creates a content type, adds a site column, associates it with a list,
and sets it as the default — the most common real-world workflow.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.contenttypes.creation_information import ContentTypeCreationInformation
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=***
)

# 1. Create a content type
info = ContentTypeCreationInformation(
    Name="Invoice Document",
    Description="For customer invoices",
)
ct = ctx.web.content_types.add(info).execute_query()
print(f"1. Created: {ct.name}  (ID: {ct.id})")

# 2. Add a site column to the content type
field = ctx.web.fields.get_by_internal_name_or_title("Title")
ct.field_links.add(field).execute_query()
print(f"2. Added field: {field.internal_name}")

# 3. Add content type to a list
target_list = ctx.web.lists.get_by_title("Documents")
target_list.content_types.add_available_content_type(ct.string_id).execute_query()
print(f"3. Added to list: {target_list.title}")

# 4. Verify — list content types on the list
list_cts = target_list.content_types.get().execute_query()
print(f"4. Content types on '{target_list.title}':")
for c in list_cts:
    print(f"   - {c.name}")