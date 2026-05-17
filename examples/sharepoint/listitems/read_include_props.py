"""Demonstrates how to retrieve list items and select specific properties to return

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
lib = ctx.web.default_document_library()
items = lib.items.get().select(["FileRef"]).top(100).execute_query()
for item in items:
    print(item.properties.get("FileRef"))
