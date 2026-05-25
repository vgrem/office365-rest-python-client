"""
List all home sites configured for the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/hubsites
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_id, test_password, test_tenant, test_username

ctx = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = Tenant(ctx).get_home_sites().execute_query()
for hs in result.value:
    print(f"  {hs.Title}  ({hs.Url})")
