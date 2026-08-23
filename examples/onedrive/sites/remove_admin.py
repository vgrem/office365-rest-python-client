"""
Remove a user's access (permission) from a SharePoint site.

Requires delegated permission Sites.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/permission-delete
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Remove a user's access (permission) from a SharePoint site")
    parser.add_argument("--site-url", required=True, help="Site URL")
    parser.add_argument("--user-email", required=True, help="User email to remove")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    site_url = args.site_url.strip()
    user_email = args.user_email.strip()

    site = client.sites.get_by_url(site_url).get().execute_query()
    target = client.users.filter(f"mail eq '{user_email}'").get().execute_query()
    if not target:
        print(f"User '{user_email}' not found.")
        return
    target_id = target[0].id

    perms = site.permissions.get().execute_query()
    for p in perms:
        for identity in p.granted_to_identities:
            if identity.user and identity.user.id == target_id:
                p.delete_object().execute_query()
                print(f"Removed {user_email} from {site.display_name}")
                return

    print(f"Permission for {user_email} not found on {site.display_name}")


if __name__ == "__main__":
    main()
