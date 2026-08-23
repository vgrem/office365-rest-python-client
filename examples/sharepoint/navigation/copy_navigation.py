"""
Copy the top navigation bar from a source site to a target site.

Recursively recreates the source site's top navigation (including sub-menus)
on the target site, replacing any existing top navigation there. Re-running is
safe — the target navigation is rebuilt from the source each time.

A Python port of PnP's ``spo-copy-hubsite-navigation`` script sample.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/navigation-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.navigation.nodes.creationinformation import NavigationNodeCreationInformation
from tests.settings import cert_path, cert_thumbprint, client_id, tenant


def _copy_node(source_node, target_nodes) -> None:
    """Create source_node under target_nodes, then recursively copy its children."""
    created = target_nodes.add(
        NavigationNodeCreationInformation(Title=source_node.title or "", Url=source_node.url or "", AsLastNode=True)
    )
    created.execute_query()
    for child in source_node.children.get().execute_query():
        _copy_node(child, created.children)


def main():
    parser = argparse.ArgumentParser(description="Copy the top navigation bar between sites")
    parser.add_argument("--source-url", required=True, help="source site URL")
    parser.add_argument("--target-url", required=True, help="target site URL")
    args = parser.parse_args()

    source = ClientContext(args.source_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target = ClientContext(args.target_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    existing = target.web.navigation.top_navigation_bar.get().execute_query()
    for node in existing:
        node.delete_object()
    target.execute_query()

    source_nodes = source.web.navigation.top_navigation_bar.get().execute_query()
    for node in source_nodes:
        _copy_node(node, target.web.navigation.top_navigation_bar)

    print(f"✓ Copied top navigation from {args.source_url} to {args.target_url}")


if __name__ == "__main__":
    main()
