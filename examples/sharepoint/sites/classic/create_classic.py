"""
Creates a classic site collection (not group-connected).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import (
    test_admin_site_url,
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

ctx = ClientContext(test_admin_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
admin = Tenant(ctx)
admin.create_site(f"{test_admin_site_url}/sites/ClassicSite", test_user_principal_name, "Classic Site").execute_query()
print("Classic site created")
