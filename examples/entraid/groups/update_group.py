"""
Update a group's properties (display name, description, visibility).

https://learn.microsoft.com/en-us/graph/api/group-update
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Update a group's properties")
    parser.add_argument("--group", required=True, help="group display name")
    parser.add_argument("--display-name", help="new display name")
    parser.add_argument("--description", help="new description")
    parser.add_argument("--visibility", choices=["Public", "Private"], help="new visibility")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    group = client.groups.get_by_name(args.group).get().execute_query()

    if args.display_name:
        group.set_property("displayName", args.display_name)
    if args.description:
        group.set_property("description", args.description)
    if args.visibility:
        group.set_property("visibility", args.visibility)

    group.update().execute_query()
    print(f"✓ Updated '{group.display_name}'")


if __name__ == "__main__":
    main()
