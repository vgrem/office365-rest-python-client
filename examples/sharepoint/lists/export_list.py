import os
import tempfile

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.file import File
from office365.sharepoint.listitems.listitem import ListItem
from tests import test_client_credentials, test_team_site_url


def print_progress(item):
    # type: (ListItem|File) -> None
    if isinstance(item, ListItem):
        print("List Item has been exported...")
    else:
        print("File has been downloaded...")


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

list_title = "Orders"
lib = ctx.web.lists.get_by_title(list_title)
export_path = os.path.join(tempfile.mkdtemp(), f"{list_title}.zip")
with open(export_path, "wb") as f:
    lib.export(f, True, print_progress).execute_query()
print(f"List has been export into {export_path} ...")
