"""
Generates a site script from an existing site.

Site scripts can be exported from an existing site and reused
to apply the same configuration to other sites.

https://learn.microsoft.com/en-us/sharepoint/dev/declarative-customization/site-design-overview
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
result = ctx.web.get_site_script(included_lists=["Shared Documents"]).execute_query()
print(result.value.JSON)
