"""Demonstrates how to retrieve a content type by name.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/contenttype
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
ct = ctx.web.content_types.get_by_name("Project Document").execute_query()
print(f"Name: {ct.name}")
print(f"Description: {ct.description}")
print(f"ID: {ct.id}")
