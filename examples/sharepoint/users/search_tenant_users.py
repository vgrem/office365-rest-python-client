"""
Search tenant users.
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_admin_site_url, test_client_credentials

ctx = ClientContext(test_admin_site_url).with_credentials(test_client_credentials)
result = ctx.search_user("SharePoint Service Administrator").execute_query()
print(result.value)
