"""
Create sharing links and send sharing invitations for files.

Two sharing patterns: anonymous/organization links and direct invitations
to specific users. Run against a freshly uploaded file so it is safe to re-run.

Requires delegated permission ``Files.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/driveitem-createlink
https://learn.microsoft.com/en-us/graph/api/driveitem-invite
"""

import argparse

from office365.graph_client import GraphClient
from tests import create_unique_name
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create sharing links and invitations for a file")
    parser.add_argument("--user", help="UPN of the user to invite (skip to omit the invitation)")
    parser.add_argument("--keep", action="store_true", help="keep the test file after the demo")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    # -- Step 1: create a test file --
    item = client.me.drive.root.upload(create_unique_name("share") + ".txt", b"Shared content\n").execute_query()
    print(f"Created: {item.name}")

    # -- Step 2: anonymous read link --
    permission = item.create_link("view", "anonymous").execute_query()
    print(f"Anonymous read link: {permission.link.webUrl}")

    # -- Step 3: organization edit link --
    permission2 = item.create_link("edit", "organization").execute_query()
    print(f"Organization edit link: {permission2.link.webUrl}")

    # -- Step 4: direct invitation --
    if args.user:
        item.invite(
            [args.user],
            send_invitation=True,
            message="Here's the file you requested.",
        ).execute_query()
        print(f"Invitation sent to: {args.user}")

    # -- Step 5: list current permissions --
    permissions = item.permissions.get().execute_query()
    print(f"\nPermissions ({len(permissions)}):")
    for p in permissions:
        inherited = " (inherited)" if p.inherited_from else ""
        print(f"  ID: {p.id}  roles: {', '.join(p.roles)}{inherited}")

    # -- Step 6: clean up --
    if not args.keep:
        item.delete_object().execute_query()
        print("\nTest file removed.")


if __name__ == "__main__":
    main()
