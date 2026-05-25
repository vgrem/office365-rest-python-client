"""Demonstrates how to add a content type to a list.

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
target_list = ctx.web.lists.get_by_title("Documents")
ct = ctx.web.content_types.add(
    ContentTypeCreationInformation(Name="Project Document", Description="For Contoso projects")
).execute_query()
target_list.content_types.add(ContentTypeCreationInformation(Name="Project Document", Id="0x0120")).execute_query()
print(f"Content type added to list: {ct.name}")
