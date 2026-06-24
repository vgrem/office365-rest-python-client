"""
Add a child navigation node (sub-menu) under an existing parent node.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

import sys

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.creationinformation import NavigationNodeCreationInformation
from tests.settings import client_id, client_secret, site_url, tenant

ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

nav = ctx.web.navigation.quick_launch.get().execute_query()
if not nav:
    sys.exit("No navigation nodes found.")

parent = nav[0]
child_info = NavigationNodeCreationInformation(
    Title="Child page",
    Url=f"{ctx.base_url}/SitePages/Child.aspx",
    AsLastNode=True,
)
child = parent.children.add(child_info).execute_query()
print(f"Child node added: {child.title} under {parent.title}")
