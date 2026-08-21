"""
Create a site script from an existing web, then bundle it into a site design.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

import argparse
import json
import uuid

from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sitedesigns.creation_info import SiteDesignCreationInfo
from office365.sharepoint.sitescripts.utility import SiteScriptUtility
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a site design from an existing web")
    parser.add_argument("--script-title", default="Exported from web", help="site script title")
    parser.add_argument("--design-title", default="Design from web", help="site design title")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # Export current web configuration as a site script
    serialized = ctx.web.get_site_script().execute_query()
    assert serialized.value.JSON is not None
    print(f"Generated site script ({len(serialized.value.JSON)} chars)")

    # Create the site script from the exported JSON
    script_result = SiteScriptUtility.create_site_script(
        ctx, args.script_title, "Auto-exported site script", json.loads(serialized.value.JSON)
    ).execute_query()

    # Create a site design that uses this script
    design_info = SiteDesignCreationInfo(
        Title=args.design_title,
        Description="Created from an existing site export",
        WebTemplate="64",
        SiteScriptIds=ClientValueCollection(uuid.UUID, [uuid.UUID(script_result.value.Id)]),
    )
    design = SiteScriptUtility.create_site_design(ctx, design_info).execute_query()
    print(f"Site design created: {design.value.Title} (ID: {design.value.Id})")


if __name__ == "__main__":
    main()
