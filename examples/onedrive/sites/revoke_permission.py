"""
Remove a specific permission (user/group) from a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-delete-permission
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    site_url = input("Site URL: ").strip()
    site = client.sites.get_by_url(site_url).get().execute_query()

    permissions = site.permissions.get().execute_query()
    print(f"Permissions on {site.display_name}:")
    for p in permissions:
        print(f"  {p.id}  roles={p.roles}")
    permission_id = input("Permission ID to remove: ").strip()

    site.permissions[permission_id].delete_object().execute_query()
    print(f"Permission {permission_id} removed from {site.display_name}.")


if __name__ == "__main__":
    main()
