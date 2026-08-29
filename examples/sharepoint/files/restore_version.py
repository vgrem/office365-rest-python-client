"""
Restore a previous version of a file by label.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Restore a previous version of a file by label")
    parser.add_argument("--file-url", default="Shared Documents/report.docx", help="server-relative file URL")
    parser.add_argument("--label", default="2.0", help="version label to restore")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.get_file_by_server_relative_path(args.file_url)

    file.versions.restore_by_label(args.label).execute_query()
    print(f"Version {args.label} restored")


if __name__ == "__main__":
    main()
