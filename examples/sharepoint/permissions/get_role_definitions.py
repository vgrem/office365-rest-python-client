"""
List all role definitions (permission levels) available on a site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/permissions-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
roles = ctx.web.role_definitions.get().execute_query()
for role in roles:
    print(f"  {role.properties['Name']}  (ID: {role.properties['Id']}, "
          f"Order: {role.properties.get('Order', '')})")
