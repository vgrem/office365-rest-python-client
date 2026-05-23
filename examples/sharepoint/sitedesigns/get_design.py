"""
Get metadata for a specific site design by ID.

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
    detail = SiteScriptUtility.get_site_design_metadata(ctx, target.Id).execute_query()
    print(f"Title: {detail.value.Title}")
    print(f"Description: {detail.value.Description}")
    print(f"WebTemplate: {detail.value.WebTemplate}")
    print(f"SiteScriptIds: {detail.value.SiteScriptIds}")
    print(f"Id: {detail.value.Id}")
