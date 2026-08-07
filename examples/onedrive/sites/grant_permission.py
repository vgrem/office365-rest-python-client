"""
Grant a user read or write access to a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-post-permissions
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    site_url = input("Site URL: ").strip()
    user_email = input("User email to grant access: ").strip()
    role = input("Role (read/write): ").strip().lower()

    site = client.sites.get_by_url(site_url).get().execute_query()
    users = client.users.filter(f"mail eq '{user_email}'").get().execute_query()
    if not users:
        print(f"User '{user_email}' not found.")
        return

    site.permissions.add(roles=[role], identity=users[0]).execute_query()
    print(f"Granted '{role}' on {site.display_name} to {user_email}")


if __name__ == "__main__":
    main()
