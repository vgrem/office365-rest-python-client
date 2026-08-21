"""
Demonstrates how to download list item attachments
"""

import argparse
import os
import tempfile

from office365.sharepoint.attachments.attachment import Attachment
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def print_progress(attachment_file: Attachment) -> None:
    print("{0} has been downloaded".format(attachment_file.server_relative_url))


def main():
    parser = argparse.ArgumentParser(description="Download list item attachments")
    parser.add_argument("--list-title", default="Company Tasks", help="list title")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )

    source_list = ctx.web.lists.get_by_title(args.list_title)
    items = source_list.items.get().execute_query()
    for item in items:
        zip_path = os.path.join(tempfile.mkdtemp(), "attachments_{0}.zip".format(item.id))
        with open(zip_path, "wb") as f:
            item.attachment_files.download(f, print_progress).execute_query()
        print("{0} attachments has been downloaded...".format(zip_path))


if __name__ == "__main__":
    main()
