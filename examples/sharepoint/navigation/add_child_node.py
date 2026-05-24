"""
Add a child navigation node (sub-menu) under an existing parent node.

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

# Get the first Quick Launch node to use as parent
nav = ctx.web.navigation.quick_launch.get().execute_query()
if nav:
    parent_id = nav[0].properties.get("Id")
    assert parent_id is not None
    parent_node = ctx.web.navigation.quick_launch.get_by_id(parent_id).get().execute_query()

    child_info = NavigationNodeCreationInformation(
        Title="Child page",
        Url=f"{ctx.base_url}/SitePages/Child.aspx",
        AsLastNode=True,
    )
    child_node = parent_node.children.add(child_info).execute_query()
    print(f"Child node added: {child_node.title} under {parent_node.title}")
