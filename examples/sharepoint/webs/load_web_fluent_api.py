"""
Demonstrates loading a SharePoint web using the fluent API.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
target_web = ctx.web.get().execute_query()
print(target_web.url)
