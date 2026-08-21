"""
Demonstrates how to rename a page
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Rename a page")
    parser.add_argument("--file-url", default="Site Pages/Home.aspx", help="server-relative file URL")
    parser.add_argument("--new-name", default="NewHome.aspx", help="new file name")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.get_file_by_server_relative_path(args.file_url)
    file.rename(args.new_name).execute_query()


if __name__ == "__main__":
    main()
