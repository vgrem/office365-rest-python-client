"""Report on site pages — list all pages with author, created date, last modified,
and promotion status.

Uses offset paging: the site pages endpoint does not return a server-side next
link, so ``get_all()``/``paged()`` cannot advance past the first page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant

PAGE_SIZE = 50


def main():
    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)

    pages = []
    offset = 0
    while True:
        batch = list(ctx.site_pages.pages.skip(offset).top(PAGE_SIZE).get().execute_query())
        if not batch:
            break
        pages.extend(batch)
        offset += PAGE_SIZE

    print(f"{'Title':40s}  {'Author':25s}  {'Created':15s}  {'Modified':15s}  {'Promoted'}")
    print("-" * 105)
    for p in pages:
        author = p.properties.get("Author", {}).get("Title", "?")[:25]
        created = str(p.properties.get("Created", ""))[:10]
        modified = str(p.properties.get("Modified", ""))[:10]
        promoted = "Y" if p.properties.get("PromotedState", 0) else ""
        print(f"{(p.properties.get('Title') or ''):40s}  {author:25s}  {created:15s}  {modified:15s}  {promoted}")

    promoted = sum(1 for p in pages if p.properties.get("PromotedState", 0))
    print(f"\nTotal: {len(pages)} pages, {promoted} promoted, {len(pages) - promoted} draft")


if __name__ == "__main__":
    main()
