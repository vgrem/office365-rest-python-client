"""
Delete term store groups, sets, and terms.

Common scenarios:
  - Reset test environment before re-importing
  - Remove obsolete taxonomy
  - Clean up after migration

Requires delegated permission Sites.ReadWrite.All.
"""

from office365.graph_client import GraphClient
from office365.runtime.client_request_exception import ClientRequestException
from tests import test_client_id, test_client_secret, test_root_site_url, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
    store = client.sites.get_by_url(test_root_site_url).term_store

    # Delete all groups (full reset)
    for g in store.groups.get().execute_query():
        try:
            g.delete_object().execute_query()
            print(f"Group '{g.display_name}' has been deleted")
        except ClientRequestException as e:
            if e.code == "notAllowed":
                print(f"Skipped: {g.display_name} — not empty, delete child sets first")
            elif e.code == "accessDenied":
                print(f"Skipped: {g.display_name} — access denied")
            else:
                print(f"Error deleting {g.display_name}: {e}")


if __name__ == "__main__":
    main()
