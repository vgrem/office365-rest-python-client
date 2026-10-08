"""
Find orphaned groups — groups without owners or without members.

Ownerless groups cannot be administered (no one can approve changes);
memberless groups are dead weight. Either is a cleanup candidate.

Requires application permission ``Group.Read.All``.

https://learn.microsoft.com/en-us/graph/api/group-list
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    groups = client.groups.get_all().execute_query()

    ownerless, memberless = [], []
    for group in groups:
        if not group.owners.get().execute_query():
            ownerless.append(group)
        if not group.members.get().execute_query():
            memberless.append(group)

    print(f"Without owners ({len(ownerless)}):")
    for group in ownerless:
        print(f"  {group.display_name}")
    print(f"\nWithout members ({len(memberless)}):")
    for group in memberless:
        print(f"  {group.display_name}")


if __name__ == "__main__":
    main()
