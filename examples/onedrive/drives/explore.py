"""
Explore your OneDrive: recent files, shared items, and followed sites.

Shows the three most common discovery patterns.

Requires delegated permission ``Files.Read``, ``Sites.Read.All``.

https://learn.microsoft.com/en-us/graph/api/drive-recent
https://learn.microsoft.com/en-us/graph/api/drive-sharedwithme
https://learn.microsoft.com/en-us/graph/api/sites-list-followed
"""

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

# 1. Recently used items
recent = client.me.drive.recent().execute_query()
print(f"Recent items ({len(recent)}):")
for item in recent:
    print(f"  {item.name}")
print()

# 2. Items shared with me
shared = client.me.drive.shared_with_me().execute_query()
print(f"Shared with me ({len(shared)}):")
for item in shared:
    print(f"  {item.name:40s}  shared by: {item.remote_item.shared.sharedBy if item.remote_item else '?'}")
print()

# 3. Followed sites
sites = client.me.followed_sites.get().execute_query()
print(f"Followed sites ({len(sites)}):")
for s in sites:
    print(f"  {s.display_name}  ({s.web_url})")
