"""Demonstrates how to retrieve list items with specific properties using the load method

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
lib = ctx.web.lists.get_by_title("Documents")
items = lib.items
ctx.load(items, ["EncodedAbsUrl"])
ctx.execute_query()
for item in items:
    print("{0}".format(item.properties.get("EncodedAbsUrl")))
