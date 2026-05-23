"""
Update an existing site design — change title, description, or linked scripts.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitedesigns.metadata import SiteDesignMetadata
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
if designs:
    target = designs[0]
    # Build update payload with new description
    update_info = SiteDesignMetadata(id_=target.Id)
    update_info.Title = target.Title
    update_info.Description = f"{target.Description} (updated)"
    update_info.WebTemplate = target.WebTemplate
    result = SiteScriptUtility.update_site_design(ctx, update_info).execute_query()
    print(f"Updated: {result.Title} — {result.Description}")
