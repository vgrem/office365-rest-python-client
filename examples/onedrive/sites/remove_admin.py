"""
Remove a user's access (permission) from a SharePoint site.

Requires delegated permission Sites.ReadWrite.All.

https://learn.microsoft.com/en-us/graph/api/permission-delete
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    site_url = input("Site URL: ").strip()
    user_email = input("User email to remove: ").strip()

    site = client.sites.get_by_url(site_url).get().execute_query()
    perms = site.permissions.get().execute_query()

    for p in perms:
        for identity in p.granted_to_identities:
            if identity.user and identity.user.email == user_email:
                p.delete_object().execute_query()
                print(f"Removed {user_email} from {site.display_name}")
                return

    print(f"Permission for {user_email} not found on {site.display_name}")


if __name__ == "__main__":
    main()
