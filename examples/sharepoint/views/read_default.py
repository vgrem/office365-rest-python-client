"""
Reads list items from a default view.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.default_document_library()
items = lib.default_view.get_items().execute_query()
for item in items:
    print(item.properties)
