"""
Disables SSL certificate verification for SharePoint requests.

⚠️ WARNING: Only use this for testing with self-signed certificates.
Never disable SSL verification in production.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = (
    ClientContext(site_url)
    .with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    .with_transport(verify=False)
)

web = ctx.web.get().execute_query()
print(web.url)
