"""Demonstrates how to read list items in a paged manner

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.collection import ListItemCollection
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def print_progress(items: ListItemCollection) -> None:
    print(f"Items read: {len(items)}")


ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)
large_list = ctx.web.lists.get_by_title("Contacts_Large")
paged_items = large_list.items.paged(1000, page_loaded=print_progress).get().execute_query()
for _, _ in enumerate(paged_items):
    pass
    # print(f"{index}: {item.id}")
