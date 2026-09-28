"""
Submit a SharePoint batch asynchronously.

``execute_batch_async`` splits the pending changes exactly like
``execute_batch`` but never blocks the event loop. With ``concurrency`` > 1 the
batches overlap, and throttling / per-sub-request retry behave the same as in
the synchronous path.

Requires delegated permission ``Sites.FullControl.All`` (writes list items).

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import asyncio

from office365.sharepoint.client_context import ClientContext
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


async def main() -> None:
    ctx = ClientContext(site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )
    target_list = ctx.web.lists.get_by_title("Company Tasks")
    for index in range(250):
        target_list.add_item({"Title": f"Task {index}"})

    await ctx.execute_batch_async(items_per_batch=100, concurrency=4)
    print(f"List items count: {target_list.item_count}")


asyncio.run(main())
