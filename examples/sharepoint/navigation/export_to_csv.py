"""
Export SharePoint navigation structure to CSV — both Quick Launch
and top nav bars with hierarchy depth.

Useful for site audits, documenting navigation, and planning
restructuring.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

import csv

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.node import NavigationNode
from tests.settings import client_id, client_secret, site_url, tenant


def write_nodes(w, parent: NavigationNode, depth: int = 0) -> None:
    """Recursively write a node and its children to CSV."""
    w.writerow([depth * "  " + (parent.title or ""), parent.url or "", depth])
    children = parent.children.get().execute_query()
    for child in children:
        write_nodes(w, child, depth + 1)


ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

with open("nav_export.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["Title", "URL", "Depth"])
    print("Quick Launch:")
    for node in ctx.web.navigation.quick_launch.get().execute_query():
        write_nodes(w, node)
    print("Top nav bar:")
    for node in ctx.web.navigation.top_navigation_bar.get().execute_query():
        write_nodes(w, node)

print("Exported to nav_export.csv")
