"""Demonstrates how to delete all list items in a list

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url


def print_progress(items_count: int) -> None:
    print("List items count: {0}".format(target_list.item_count))


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
target_list = ctx.web.lists.get_by_title("Company Tasks")
target_list.clear().get().execute_batch()
print("List items count: {0}".format(target_list.item_count))
