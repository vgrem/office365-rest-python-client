"""
Get recently modified files from the current user's recent file list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_client_secret, test_tenant, test_site_url

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
recent = ctx.web.recent_files.get().execute_query()
for item in recent:
    print(f"{item.name}  ({item.last_modified})")
