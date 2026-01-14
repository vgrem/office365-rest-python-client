"""Demonstrates how to download list item attachments"""

import os
import tempfile

from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.client_context import ClientContext
from tests import test_client_credentials, test_team_site_url


def print_progress(attachment_file):
    # type: (Attachment) -> None
    print(f"{attachment_file.server_relative_url} has been downloaded")


ctx = ClientContext(test_team_site_url).with_credentials(test_client_credentials)

list_title = "Company Tasks"
source_list = ctx.web.lists.get_by_title(list_title)
items = source_list.items.get().execute_query()
for item in items:
    zip_path = os.path.join(tempfile.mkdtemp(), f"attachments_{item.id}.zip")
    with open(zip_path, "wb") as f:
        item.attachment_files.download(f, print_progress).execute_query()
    print(f"{zip_path} attachments has been downloaded...")
