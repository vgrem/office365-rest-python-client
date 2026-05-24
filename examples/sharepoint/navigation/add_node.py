"""
Add a navigation node to the Quick Launch or top navigation bar.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.creationinformation import NavigationNodeCreationInformation
from tests import test_client_id, test_password, test_site_url, test_tenant, test_username

ctx = ClientContext(test_site_url).with_username_and_password(
    tenant=test_tenant,
    client_id=test_client_id,
    username=test_username,
    password=test_password,
)

# Add to Quick Launch
node_info = NavigationNodeCreationInformation(
    Title="Contoso",
    Url="https://contoso.sharepoint.com",
    IsExternal=True,
    AsLastNode=True,
)
node = ctx.web.navigation.quick_launch.add(node_info).execute_query()
print(f"Node added: {node.title} (ID: {node.id or ''})")
