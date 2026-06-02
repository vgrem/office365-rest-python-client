"""
Get and set property bag values on a web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
web = ctx.web.get().execute_query()

# Read all properties
all_props = web.all_properties.get().execute_query()
for key, value in all_props.properties.items():
    if key.startswith("Custom_"):
        print(f"  {key}: {value}")
