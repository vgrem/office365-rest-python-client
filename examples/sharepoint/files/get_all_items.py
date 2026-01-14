"""Enumerates files and folders within a library"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from office365.sharepoint.listitems.listitem import ListItem
from tests import test_client_credentials, test_team_site_url

ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)
doc_lib = ctx.web.default_document_library()
items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get_all().execute_query()
for idx, item in enumerate(items):  # type: int, ListItem
    if item.file_system_object_type == FileSystemObjectType.Folder:
        print(f"({idx} of {len(items)})  Folder: {item.folder.serverRelativeUrl}")
    else:
        print(f"({idx} of {len(items)}) File: {item.file.serverRelativeUrl}")
