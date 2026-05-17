"""
Connect to SharePoint using device code flow.

Useful for devices or environments without a web browser.
The user authenticates on another device by visiting a URL
and entering the displayed code.

See https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_device_flow(test_tenant, test_client_id)
me = ctx.web.current_user.get().execute_query()
print(me.login_name)
web = ctx.web.get().execute_query()
print(web.title)
