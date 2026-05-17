"""Demonstrates how to retrieve all list items from a large list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.collection import ListItemCollection
from tests import test_client_credentials, test_team_site_url


def print_progress(items: ListItemCollection) -> None:
    print(f"Items read: {len(items)}")


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
large_list = ctx.web.lists.get_by_title("Contacts_Large")
all_items = large_list.items.get_all(5000, print_progress).execute_query()
print(f"Total items count: {len(all_items)}")
