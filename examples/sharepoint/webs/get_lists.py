"""Site lists inventory report.

Enumerates the lists of the site, splits them into system vs custom, and
prints per-list stats (item count, template, created date, hidden flag)
plus a summary.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/site-operations
"""

from __future__ import annotations

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.lists.list import List
from office365.sharepoint.lists.templates.type import ListTemplateType
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def _template_name(template_id: int) -> str:
    try:
        return ListTemplateType(template_id).name
    except ValueError:
        return str(template_id)


def _print_group(title: str, lists: list[List]) -> None:
    print(f"\n{title} ({len(lists)}):")
    for lst in sorted(lists, key=lambda item: item.item_count or 0, reverse=True):
        print(
            f"  {lst.title:42s} items={lst.item_count or 0:>6}  "
            f"template={_template_name(lst.base_template or 0):18s} created={lst.created:%Y-%m-%d}"
        )


def main():
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    lists = (
        ctx.web.lists.select(["IsSystemList", "ItemCount", "Hidden", "BaseTemplate", "Title", "Created"])
        .get()
        .execute_query()
    )
    system = [lst for lst in lists if lst.is_system_list is True]
    custom = [lst for lst in lists if lst.is_system_list is False]

    _print_group("System lists", system)
    _print_group("Custom lists", custom)

    total_items = sum(lst.item_count or 0 for lst in lists)
    print(
        f"\nTotal: {len(lists)} lists, {sum(1 for lst in lists if lst.hidden)} hidden, "
        f"{sum(1 for lst in lists if lst.item_count and lst.item_count > 0)} non-empty, {total_items} list items"
    )


if __name__ == "__main__":
    main()
