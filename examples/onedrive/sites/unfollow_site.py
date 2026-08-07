"""
Unfollow a SharePoint site.

Requires delegated permission ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/site-unfollow
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

site_url = input("Site URL: ").strip()
site = client.sites.get_by_url(site_url).get().execute_query()
client.me.unfollow_site(site).execute_query()
print(f"Unfollowed {site.display_name}.")
