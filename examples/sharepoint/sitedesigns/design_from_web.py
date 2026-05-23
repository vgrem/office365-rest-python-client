"""
Create a site script from an existing web, then bundle it into a site design.

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

# Export current web configuration as a site script
serialized = SiteScriptUtility.get_site_script_from_web(ctx, test_site_url).execute_query()
print(f"Generated site script ({len(serialized.value.JSON)} chars)")

# Create the site script from the exported JSON
import json

script_result = SiteScriptUtility.create_site_script(
    ctx, "Exported from web", "Auto-exported site script", json.loads(serialized.value.JSON)
).execute_query()

# Create a site design that uses this script
design_info = SiteDesignCreationInfo(
    Title="Design from web",
    Description="Created from an existing site export",
    WebTemplate="64",
    SiteScriptIds=[uuid.UUID(script_result.value.Id)],
)
design = SiteScriptUtility.create_site_design(ctx, design_info).execute_query()
print(f"Site design created: {design.value.Title} (ID: {design.value.Id})")
