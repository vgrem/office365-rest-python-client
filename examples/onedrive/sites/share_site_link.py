"""
Create an anonymous sharing link for a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-post-permissions
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, password, site_url, tenant, user_principal, username


def main():
    parser = argparse.ArgumentParser(description="Create an anonymous sharing link for a SharePoint site")
    parser.add_argument("--site-url", default=site_url, help="site URL to share")
    parser.add_argument("--user-principal", default=user_principal, help="user principal name to grant access to")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

    user = client.users.get_by_principal_name(args.user_principal)
    site = client.sites.get_by_url(args.site_url).get().execute_query()
    permission = site.permissions.add(roles=["owner"], identity=user).execute_query()
    print(f"Created sharing link: {permission.link.webUrl}")


if __name__ == "__main__":
    main()
