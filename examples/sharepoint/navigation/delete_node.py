"""
Delete a navigation node by ID.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)
nav = ctx.web.navigation.top_navigation_bar.get().execute_query()
if nav:
    node = nav[0]
    node_id = node.id
    assert node_id is not None
    target = ctx.web.navigation.top_navigation_bar.get_by_id(node_id).get().execute_query()
    target.delete_object().execute_query()
    print(f"Deleted navigation node ID: {node_id}")
