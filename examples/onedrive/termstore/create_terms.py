"""
Create term store groups, sets, and terms.

The term store is the managed metadata service for consistent tagging across
SharePoint and OneDrive. This example creates a group, a set, and terms, then
cleans up after itself.

Requires delegated permission ``Sites.ReadWrite.All`` (or application
``TermStore.ReadWrite.All``).

https://learn.microsoft.com/en-us/graph/api/termstore-group-post
https://learn.microsoft.com/en-us/graph/api/termstore-set-post-children
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, client_secret, root_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Create term store groups, sets and terms")
    parser.add_argument("--keep", action="store_true", help="keep the group after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    store = client.sites.get_by_url(root_site_url).term_store

    # -- Step 1: list existing groups --
    groups = store.groups.get().execute_query()
    print(f"Existing term store groups ({len(groups)}):")
    for g in groups:
        print(f"  {g.display_name}")

    # -- Step 2: create a group --
    group = store.groups.add(create_unique_name("SDK")).execute_query()
    print(f"\nGroup created: '{group.display_name}'")

    # -- Step 3: add a set --
    term_set = group.sets.add("Project Tags").execute_query()
    print(f"  Set: '{term_set.display_name}'")

    # -- Step 4: add terms to the set --
    for term_name in ["Urgent", "In Progress", "Completed"]:
        term = term_set.children.add(label=term_name).execute_query()
        print(f"    Term: '{term.display_name}'")

    if not args.keep:
        group.delete_object().execute_query()
        print("\nGroup removed.")


if __name__ == "__main__":
    main()
