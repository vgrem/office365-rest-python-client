"""Demonstrates how to filter list items by filename

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_site_url

ctx = ClientContext(test_site_url).with_credentials(test_client_credentials)
result = ctx.web.lists.get_by_title("Documents").items.get().filter("FileLeafRef eq 'report.csv'").execute_query()
for item in result:
    print(item.properties)
