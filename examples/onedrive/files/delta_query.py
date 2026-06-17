"""
Delta query — track changes to files and folders over time.

Requires delegated permission Files.Read.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    changes = client.me.drive.root.delta.get().execute_query()
    for item in changes:
        if item.deleted:
            tag = "deleted"
        elif (
            item.created_date_time
            and item.last_modified_date_time
            and item.created_date_time == item.last_modified_date_time
        ):
            tag = "new"
        else:
            tag = "updated"
        print(f"  [{tag}] {item.name}")


if __name__ == "__main__":
    main()
