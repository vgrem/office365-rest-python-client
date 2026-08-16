"""Demonstrates how to export a SharePoint list as a package (.zip)

Official documentation: https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/list-operations
"""

import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.exporter import ExportListProgress
from tests.settings import cert_path, cert_thumbprint, client_id, site_url, tenant


def print_progress(progress: ExportListProgress) -> None:
    if isinstance(progress.current_item, ListItem):
        print("List Item has been exported...")
    else:
        print("File has been downloaded...")
    print(f"Progress: {progress.processed_items}/{progress.total_items} items")


ctx = ClientContext(site_url).with_client_certificate(
    tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
)

list_title = "Orders"
lib = ctx.web.lists.get_by_title(list_title)
export_path = os.path.join(tempfile.mkdtemp(), f"{list_title}.zip")
with open(export_path, "wb") as f:
    lib.export(f, True, print_progress).execute_query()
print(f"List has been export into {export_path} ...")
