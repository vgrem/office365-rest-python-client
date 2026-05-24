"""
Update a navigation node — rename, change URL, or toggle visibility.

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
nav = ctx.web.navigation.quick_launch.get().execute_query()
if nav:
    node = nav[0]
    old_title = node.title
    node.title = f"{old_title} (updated)"
    node.update().execute_query()
    print(f"Node updated: {old_title} -> {node.title}")
