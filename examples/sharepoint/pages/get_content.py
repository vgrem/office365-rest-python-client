"""Get the canvas and layout web part content of a site page.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, team_site_url, tenant

PREVIEW_LEN = 128


def _preview(value: str) -> str:
    """First PREVIEW_LEN characters of a content block, with an ellipsis when truncated."""
    return value[:PREVIEW_LEN] + ("..." if len(value) > PREVIEW_LEN else "")


def main():
    parser = argparse.ArgumentParser(description="Get a site page's canvas and layout content")
    parser.add_argument("--file-name", default="Home.aspx", help="page file name (default: Home.aspx)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_secret(tenant, client_id, client_secret)
    page = ctx.site_pages.pages.get_by_name(args.file_name).execute_query()

    canvas = page.canvas_content or ""
    layout = page.layout_web_parts_content or ""
    print(f"Canvas content ({len(canvas)} chars):")
    print(_preview(canvas))
    print(f"\nLayout web parts content ({len(layout)} chars):")
    print(_preview(layout))


if __name__ == "__main__":
    main()
