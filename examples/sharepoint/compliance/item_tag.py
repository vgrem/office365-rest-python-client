"""
Apply a compliance tag (retention label) to a specific list item.

Applies the tag with hold — the item is placed under a retention hold.

Requires ``Sites.ReadWrite.All``.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Apply a compliance tag to a list item")
    parser.add_argument("--tag", required=True, help="Compliance tag name")
    parser.add_argument("--list-title", default="Documents", help="List containing the item")
    parser.add_argument("--item-id", type=int, required=True, help="Item id")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    tag = ctx.site.get_available_tag(args.tag).execute_query().value
    if not tag or not tag.TagName:
        raise SystemExit(f"Tag '{args.tag}' not found among available tags.")

    item = ctx.web.lists.get_by_title(args.list_title).items.get_by_id(args.item_id)
    item.set_compliance_tag_with_hold(tag.TagName).execute_query()
    print(f"Compliance tag '{args.tag}' applied to item {args.item_id} (with hold).")


if __name__ == "__main__":
    main()
