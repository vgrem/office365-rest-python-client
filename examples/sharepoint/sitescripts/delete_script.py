"""
Delete a site script by ID.

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
if result.value:
    target = result.value[0]
    assert target.Id is not None
    SiteScriptUtility.delete_site_script(ctx, target.Id).execute_query()
    print(f"Deleted site script: {target.Title} (ID: {target.Id})")
