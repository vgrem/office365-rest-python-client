"""Page through all site pages using client-driven (offset) paging.

The ``SP.Publishing.SitePageService/pages`` endpoint does not return a
server-side next link (unlike the classic list REST API), so server-driven
``paged()`` cannot advance beyond the first page. Use offset paging instead.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Page through all site pages by offset")
    parser.add_argument("--page-size", type=int, default=5, help="pages per request (default: 5)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    offset, total = 0, 0
    while True:
        batch = list(ctx.site_pages.pages.skip(offset).top(args.page_size).get().execute_query())
        if not batch:
            break
        total += len(batch)
        for page in batch:
            print(f"  {page.file_name}")
        print(f"  -- {total} pages so far")
        offset += args.page_size

    print(f"\nTotal site pages: {total}")


if __name__ == "__main__":
    main()
