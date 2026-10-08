"""
Create a Microsoft 365 group (with a mailbox, calendar, and Teams-ready).

The calling user is added as owner when no owner is supplied.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/group-post-groups
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    group = client.groups.create_m365(create_unique_name("Group")).execute_query()
    print(f"Created: {group.display_name} ({group.mail})")

    group.delete_object(permanent_delete=True).execute_query()
    print("Removed.")


if __name__ == "__main__":
    main()
