"""
Set a property bag value on a web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

ctx = ClientContext(site_url).with_username_and_password(tenant, client_id, username, password)
web = ctx.web
web.set_property("AllProperties", {"Custom_MyKey": "MyValue"}).update().execute_query()
print("Property bag updated")
