"""
Migrate classic blog posts to modern site pages.

Reads each post from the classic blog "Posts" list, creates a modern page on
the target site, copies the post title and body into a text web part, then
publishes the page — optionally promoting it to news.

This is a practical equivalent of PnP's ``ConvertTo-PnPPage -BlogPage``: the
PnP cmdlet wraps a large client-side transformation engine, while this example
uses the standard site-page APIs to move each post's content.

Requires read access on the source site and Site Owner on the target site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/site-pages-api-reference
"""

import argparse
import html
import json
import sys
import uuid

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username

TEXT_WEB_PART_ID = "cbe6b93c-a89d-4b1c-8b09-a1e2455f0b9c"


def _text_web_part_canvas(body_html: str) -> str:
    """Build modern page canvas content containing a single text web part."""
    control_data = {"position": {"layoutIndex": 0}}
    inner_html = (
        '<div data-sp-canvascontrol="" data-sp-canvasdataversion="1.0" '
        f'data-sp-controldata="{html.escape(json.dumps(control_data))}">'
        f'<div data-sp-rte="">{body_html}</div></div>'
    )
    canvas = [
        {
            "id": str(uuid.uuid4()),
            "anchor": f"section_{uuid.uuid4().hex}",
            "controlType": 3,
            "pageSettingsSlice": {"isDefaultTemplate": True, "isVerticalSection": False},
            "webPartId": TEXT_WEB_PART_ID,
            "innerHtml": inner_html,
        }
    ]
    return json.dumps(canvas)


def _modernize_post(target_ctx: ClientContext, title: str, body_html: str, as_news: bool) -> None:
    # Deferred: create, set content, publish, and optionally promote to news —
    # all queued (via after_execute) and executed with a single execute_query().
    canvas = _text_web_part_canvas(body_html)
    page = target_ctx.site_pages.pages.add()

    def _apply_content(_) -> None:
        page.save_draft(title=title, canvas_content=canvas)
        page.publish()
        if as_news:
            page.promote_to_news()

    page.after_execute(_apply_content)


def main():
    parser = argparse.ArgumentParser(description="Migrate classic blog posts to modern site pages")
    parser.add_argument("--source-url", default=site_url, help="classic blog site URL")
    parser.add_argument("--target-url", default=site_url, help="modern target site URL")
    parser.add_argument("--list", default="Posts", help="blog list title")
    parser.add_argument("--as-news", action="store_true", help="promote each migrated page to news")
    args = parser.parse_args()

    source = ClientContext(args.source_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    target = ClientContext(args.target_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    posts = source.web.lists.get_by_title(args.list).items.get().execute_query()
    if not posts:
        sys.exit(f"No posts found in list '{args.list}'.")

    print(f"Migrating {len(posts)} blog post(s) to {args.target_url}...")
    migrated = 0
    for post in posts:
        title = post.properties.get("Title") or "Blog post"
        body = post.properties.get("Body") or ""
        _modernize_post(target, title, body, args.as_news)
        migrated += 1

    target.execute_query()
    print(f"✓ {migrated} page(s) created and published")
    if args.as_news:
        print("  promoted to news")
    print("Blog migration complete.")


if __name__ == "__main__":
    main()
