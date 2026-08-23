"""
Delete term store groups, sets, and terms.

Common scenarios:
  - Reset a test environment before re-importing
  - Remove obsolete taxonomy
  - Clean up after a migration

Requires delegated permission ``Sites.ReadWrite.All`` (or application
``TermStore.ReadWrite.All``).

https://learn.microsoft.com/en-us/graph/api/termstore-group-delete
"""

import argparse

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests.settings import client_id, client_secret, root_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Delete term store groups")
    parser.add_argument("--prefix", default="SDK_", help="only delete groups whose name starts with this prefix")
    parser.add_argument("--dry-run", action="store_true", help="list matching groups without deleting")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    store = client.sites.get_by_url(root_site_url).term_store

    targets = [g for g in store.groups.get().execute_query() if (g.display_name or "").startswith(args.prefix)]
    print(f"Matching groups ({len(targets)}):")
    for g in targets:
        print(f"  {g.display_name}")
    if args.dry_run:
        return

    for g in targets:
        try:
            g.delete_object().execute_query()
            print(f"Deleted '{g.display_name}'")
        except ClientRequestException as e:
            if e.code == "notAllowed":
                print(f"Skipped '{g.display_name}' — not empty, delete child sets first")
            elif e.code == "accessDenied":
                print(f"Skipped '{g.display_name}' — access denied")
            else:
                print(f"Error deleting '{g.display_name}': {e}")


if __name__ == "__main__":
    main()
