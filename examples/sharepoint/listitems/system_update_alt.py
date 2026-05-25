"""Demonstrates how to update a list item using system update

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

import sys

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

target_list = ctx.web.lists.get_by_title("Documents")
items = target_list.items.get().filter("FSObjType eq 0").top(1).execute_query()
if len(items) == 0:
    sys.exit("No items were found")

item = items[0]
item.set_property("Title", "Some title goes here 123..")
item.system_update().execute_query()
