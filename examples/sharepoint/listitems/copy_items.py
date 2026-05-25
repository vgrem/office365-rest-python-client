"""Demonstrates how to copy list items from one site to another

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-item-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_team_site_url, test_tenant, test_username

source_site_url = test_site_url
target_site_url = test_team_site_url

source_ctx = ClientContext(source_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
source_items = source_ctx.web.lists.get_by_title("Tasks").items.get().top(10).execute_query()

target_ctx = ClientContext(target_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
target_list = target_ctx.web.lists.get_by_title("Tasks")
for source_item in source_items:
    props = {k: v for k, v in source_item.properties.items() if k not in ["PredecessorsId", "Id", "ID"]}
    target_list.add_item(props).execute_query()
