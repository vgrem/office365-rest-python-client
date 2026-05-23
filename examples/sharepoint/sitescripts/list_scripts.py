"""
List all site scripts in the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = SiteScriptUtility.get_site_scripts(ctx).execute_query()
for s in result.value:
    print(f"  {s.Title}  (ID: {s.Id}, Version: {s.Version})")
print(f"Total: {len(result.value)} site script(s)")
