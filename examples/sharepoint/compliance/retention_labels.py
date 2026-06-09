"""
Compliance tags (retention labels) — list available tags, check
applied tags on lists and items, and set retention compliance tags.

Compliance teams use this for data retention governance across
SharePoint sites: apply "Keep for 7 years" or "Delete after 30 days"
labels to lists and documents.

Requires delegated permission ``Sites.ReadWrite.All`` for read
operations; ``Sites.FullControl.All`` to set compliance tags.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/compliance/compliance-tag-rest-api
"""

import sys

from office365.sharepoint.client_context import ClientContext
from tests import test_site_url, test_client_id, test_client_secret, test_tenant

TAG_NAME = "Financial Records"  # Name of a compliance tag to apply


def main():
    ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)

    # -- Step 1: list all available compliance tags in the site --
    web = ctx.web.get().execute_query()
    site = ctx.site.get().execute_query()

    tags = site.get_available_tags().execute_query()
    print(f"Available compliance tags ({len(tags.value)}):\n")

    for tag in tags.value:
        display_name = tag.TagName or tag.DisplayName or "(unnamed)"
        auto_delete = tag.AutoDelete or False
        block_delete = tag.BlockDelete or False
        block_edit = tag.BlockEdit or False
        print(f"  {display_name:40s}  "
              f"auto_delete={auto_delete}  "
              f"block_delete={block_delete}  "
              f"block_edit={block_edit}")

    # -- Step 2: get compliance tag on a target list --
    target_list = ctx.web.lists.get_by_title("Documents")
    try:
        tag_info = target_list.get_compliance_tag().execute_query()
        if tag_info and tag_info.value:
            t = tag_info.value
            print(f"\nList 'Documents' compliance tag: {t.TagName or t.DisplayName or '(none)'}")
        else:
            print(f"\nList 'Documents' has no compliance tag set.")
    except Exception as e:
        print(f"\n  (compliance tag read not available: {e})")

    # -- Step 3: apply a compliance tag to a list --
    # Find the tag ID from available tags
    target_tag = None
    for tag in tags.value:
        name = tag.TagName or tag.DisplayName or ""
        if TAG_NAME.lower() in name.lower():
            target_tag = tag.tagId
            break

    if target_tag:
        print(f"\nApplying compliance tag '{TAG_NAME}' to 'Documents' list...")
        target_list.set_compliance_tag(tag_id=target_tag).execute_query()
        print("  ✓ Compliance tag applied.")
    else:
        print(f"\n  Tag '{TAG_NAME}' not found among available tags — skipping apply.")
        if tags.value:
            first_tag = tags.value[0]
            print(f"  To try with a different tag, change TAG_NAME to: {first_tag.TagName or first_tag.DisplayName}")

    # -- Step 4: apply a compliance tag with hold to a specific file --
    if target_tag:
        try:
            list_items = target_list.items.top(1).get().execute_query()
            if list_items:
                item = list_items[0]
                item.set_compliance_tag_with_hold(target_tag).execute_query()
                print(f"  ✓ Compliance tag with hold applied to item: {item.properties.get('Title', item.id)}")
        except Exception as e:
            print(f"  (item tag apply not available: {e})")


if __name__ == "__main__":
    main()
