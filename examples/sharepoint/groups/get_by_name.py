"""Demonstrates how to retrieve a site group by name.

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/group
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
g = ctx.web.site_groups.get_by_name("Team Site Members").execute_query()
print(f"Name: {g.title}")
print(f"ID: {g.id}")
print(f"Owner: {g.owner_title}")
print(f"Members: {g.users.get().execute_query().count}")