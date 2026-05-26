"""
Disables SSL certificate verification for SharePoint requests.

⚠️ WARNING: Only use this for testing with self-signed certificates.
Never disable SSL verification in production.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = (
    ClientContext(test_site_url)
    .with_username_and_password(
        tenant=test_tenant,
        client_id=test_client_id,
        username=test_username,
        password=test_password,
    )
    .with_transport(verify=False)
)

web = ctx.web.get().execute_query()
print(web.url)
