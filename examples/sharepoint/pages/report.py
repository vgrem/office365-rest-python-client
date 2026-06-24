"""
Report on site pages — list all pages with author, created date,
last modified, and promotion status.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant

ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

pages = ctx.site_pages.pages.get().execute_query()
print(f"{'Title':40s}  {'Author':25s}  {'Created':15s}  {'Modified':15s}  {'Promoted'}")
print("-" * 105)
for p in pages:
    author = p.properties.get("Author", {}).get("Title", "?")[:25]
    created = str(p.properties.get("Created", ""))[:10]
    modified = str(p.properties.get("Modified", ""))[:10]
    promoted = "Y" if p.promoted_state and p.promoted_state != 0 else ""
    print(f"{p.title or '':40s}  {author:25s}  {created:15s}  {modified:15s}  {promoted}")
