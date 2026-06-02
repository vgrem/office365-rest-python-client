"""
Restore an item from the site recycle bin.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(test_tenant, test_client_id, test_username, test_password)
items = ctx.web.recycle_bin.get().execute_query()
if len(items) > 0:
    item = items[0]
    item.restore().execute_query()
    print(f"Restored: {item.title}")
