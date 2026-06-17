"""
Delta query — track changes to files and folders over time.

Requires delegated permission Files.Read.
"""

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    changes = client.me.drive.root.delta.get().execute_query()
    for item in changes:
        if item.deleted:
            print(f"  [deleted] {item.name}")
            continue
        if (
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
