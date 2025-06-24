import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.exporter import ExportListProgress
from tests import test_client_credentials, test_team_site_url


def print_progress(progress: ExportListProgress) -> None:
    if isinstance(progress.current_item, ListItem):
        print("List Item has been exported...")
    else:
        print("File has been downloaded...")
    print(f"Progress: {progress.processed_items}/{progress.total_items} items")


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

list_title = "Orders"
lib = ctx.web.lists.get_by_title(list_title)
export_path = os.path.join(tempfile.mkdtemp(), "{0}.zip".format(list_title))
with open(export_path, "wb") as f:
    lib.export(f, True, print_progress).execute_query()
print("List has been export into {0} ...".format(export_path))
