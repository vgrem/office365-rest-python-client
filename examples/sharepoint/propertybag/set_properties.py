"""
Set a property bag value on a web.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(test_tenant, test_client_id, test_username, test_password)
web = ctx.web.get().execute_query()
web.set_property("AllProperties", {"Custom_MyKey": "MyValue"}).update().execute_query()
print("Property bag updated")
