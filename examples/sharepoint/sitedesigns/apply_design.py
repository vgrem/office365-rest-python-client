"""
Apply a site design asynchronously to a target site.

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
result = SiteScriptUtility.get_site_designs(ctx).execute_query()
if result.value:
    target = result.value[0]
    assert target.Id is not None
    task = SiteScriptUtility.add_site_design_task(ctx, test_site_url, target.Id).execute_query()
    print(f"Site design '{target.Title}' applied (task ID: {task.value.ID})")
