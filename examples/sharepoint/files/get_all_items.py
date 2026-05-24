"""
Enumerates files and folders within a library
"""

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.system_object_type import FileSystemObjectType
from tests import test_client_id, test_client_secret, test_site_url, test_tenant

ctx = ClientContext(test_site_url).with_client_secret(test_tenant, test_client_id, test_client_secret)
doc_lib = ctx.web.default_document_library()
items = doc_lib.items.select(["FileSystemObjectType"]).expand(["File", "Folder"]).get_all().execute_query()
for idx, item in enumerate(items):
    if item.file_system_object_type == FileSystemObjectType.Folder:
        print(f"({idx} of {len(items)})  Folder: {item.folder.server_relative_url}")
    else:
        print(f"({idx} of {len(items)}) File: {item.file.server_relative_url}")
