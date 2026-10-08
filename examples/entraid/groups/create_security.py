"""
Create a security group (no mailbox or calendar).

Security groups control access to resources; Microsoft 365 groups add a
mailbox, calendar, and Teams.

Requires delegated permission ``Group.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/group-post-groups
"""

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    group = client.groups.create_security(
        create_unique_name("SecurityGroup"),
        description="Access control for Project Alpha",
    ).execute_query()
    print(f"Created: {group.display_name} ({group.id})")

    group.delete_object(permanent_delete=True).execute_query()
    print("Removed.")


if __name__ == "__main__":
    main()
