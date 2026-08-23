"""
Export all modern site pages to HTML files (text content only).

Reads each page and writes its title plus canvas content (the raw HTML in the
``CanvasContent1`` field, exposed as ``canvas_content``) to a local .html file.
Files, images, and videos embedded in the pages are not exported.

Uses offset paging: the site pages endpoint does not return a server-side next
link, so ``get_all()``/``paged()`` cannot advance past the first page.

A Python port of PnP's ``spo-export-page-html`` script sample:
https://github.com/pnp/script-samples/tree/main/scripts/spo-export-page-html

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse
import sys
from pathlib import Path

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant

PAGE_SIZE = 50


def main():
    parser = argparse.ArgumentParser(description="Export modern site pages to HTML files")
    parser.add_argument("--site-url", default=site_url, help="site URL")
    parser.add_argument("--output", default="site_pages", help="output directory for the .html files")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    pages = []
    offset = 0
    while True:
        batch = list(ctx.site_pages.pages.skip(offset).top(PAGE_SIZE).get().execute_query())
        if not batch:
            break
        pages.extend(batch)
        offset += PAGE_SIZE

    pages = [page for page in pages if page.file_name and page.file_name.endswith(".aspx")]
    if not pages:
        sys.exit("No modern pages found.")

    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    for page in pages:
        title = page.properties.get("Title") or ""
        content = page.canvas_content or ""
        filename = page.file_name.replace(".aspx", ".html")
        html = f"<div><h1>{title}</h1></div>{content}"
        (out_dir / filename).write_text(html, encoding="utf-8")
        print(f"  ✓ {filename}")

    print(f"\nExported {len(pages)} page(s) to {out_dir}")


if __name__ == "__main__":
    main()
