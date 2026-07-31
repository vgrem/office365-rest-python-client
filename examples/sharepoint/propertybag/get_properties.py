"""
Get and set property bag values on a web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
web = ctx.web.get().execute_query()

# Read all properties
all_props = web.all_properties.get().execute_query()
for key, value in all_props.properties.items():
    if key.startswith("Custom_"):
        print(f"  {key}: {value}")
