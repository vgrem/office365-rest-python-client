"""
Grant or revoke access rights for principals on a site design.

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
designs = SiteScriptUtility.get_site_designs(ctx).execute_query()
if designs:
    target = designs[0]
    assert target.Id is not None

    # Grant view rights to a user
    SiteScriptUtility.grant_site_design_rights(
        ctx, target.Id, ["user@contoso.com"], 1  # 1 = View
    ).execute_query()
    print(f"Rights granted on '{target.Title}'")

    # List current rights
    principals = SiteScriptUtility.get_site_design_rights(ctx, target.Id).execute_query()
    for p in principals:
        print(f"  Principal: {p.properties.get('PrincipalName', '')}")
