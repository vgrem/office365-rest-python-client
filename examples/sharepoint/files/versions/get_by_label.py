"""
Retrieves a specific version of a file by version label.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve a file version by label")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    parser.add_argument("--label", default="1.0", help="version label")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    version = ctx.web.get_file_by_server_relative_path(args.file_url).versions.get_by_label(args.label).execute_query()

    print(version)


if __name__ == "__main__":
    main()
