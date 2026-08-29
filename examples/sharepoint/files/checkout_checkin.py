"""
Check out a file, edit it, and check it back in.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.files.checkin_type import CheckinType
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Check out a file, edit it, and check it back in")
    parser.add_argument("--file-url", default="Shared Documents/draft.docx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.get_file_by_server_relative_path(args.file_url)

    file.checkout().execute_query()
    print("File checked out")

    # Edit the file content
    content = b"Updated content"
    file.save_binary_stream(content).execute_query()

    file.checkin("Updated via API", CheckinType.MajorCheckIn).execute_query()
    print("File checked in")


if __name__ == "__main__":
    main()
