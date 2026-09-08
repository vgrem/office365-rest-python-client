"""Page through all site pages.

The ``SP.Publishing.SitePageService/pages`` endpoint does not return a
server-side next link (unlike the classic list REST API), so paging falls
back to client-driven offset requests automatically: ``paged(page_size)``
keeps fetching subsequent pages via ``$skip`` until a short/empty page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Page through all site pages")
    parser.add_argument("--page-size", type=int, default=5, help="pages per request (default: 5)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    total = 0
    pages = ctx.site_pages.pages.paged(args.page_size).get().execute_query()
    for page in pages:
        total += 1
        print(f"  {page.file_name}")
    print(f"\nTotal site pages: {total}")


if __name__ == "__main__":
    main()
