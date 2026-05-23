"""
Create a site design that bundles site scripts for applying customizations.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import uuid

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# First create a site script
site_script = {
    "$schema": "schema.json",
    "actions": [{"verb": "applyTheme", "themeName": "Contoso Theme"}],
    "bindata": {},
    "version": 1,
}
script_result = SiteScriptUtility.create_site_script(
    ctx, "Contoso theme script", "Applies the Contoso branding theme", site_script
).execute_query()
script_id = script_result.value.Id

# Bundle it into a site design
design_info = SiteDesignCreationInfo(
    Title="Contoso site",
    Description="Standard Contoso team site with branding",
    WebTemplate="64",  # 64 = team site, 68 = communication site
    SiteScriptIds=[uuid.UUID(script_id)],
)
design = SiteScriptUtility.create_site_design(ctx, design_info).execute_query()
print(f"Site design created: {design.value.Title} (ID: {design.value.Id})")
