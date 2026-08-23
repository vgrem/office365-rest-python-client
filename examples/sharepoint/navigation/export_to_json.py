"""
Export the top navigation bar structure to a JSON file.

Recursively captures every top-level node and its sub-menus as a nested tree.

A Python port of PnP's ``spo-export-topnavbar-including-translations`` script
sample (without the multilingual title resources).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

import argparse
import json
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def _node_to_dict(node):
    """Serialize a navigation node and its children as a nested dict."""
    return {
        "id": node.id,
        "title": node.title,
        "url": node.url,
        "children": [_node_to_dict(child) for child in node.children.get().execute_query()],
    }


def main():
    parser = argparse.ArgumentParser(description="Export the top navigation bar to JSON")
    parser.add_argument("--site-url", default=site_url, help="site URL")
    parser.add_argument("--output", default="top_navigation.json", help="output JSON file")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    nav = ctx.web.navigation.top_navigation_bar.get().execute_query()
    if not nav:
        sys.exit("No top navigation nodes found.")

    tree = [_node_to_dict(node) for node in nav]
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(tree, f, indent=2)
    print(f"✓ Exported {len(nav)} top-level node(s) to {args.output}")


if __name__ == "__main__":
    main()
