"""Demonstrates how to list all site groups.

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
groups = ctx.web.site_groups.get().execute_query()
for g in groups:
    print(f"  {g.title}  (ID: {g.id})")
print(f"Total: {len(groups)} groups")