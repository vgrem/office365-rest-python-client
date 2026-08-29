"""
Retrieves file extended properties (accessible via associated ListItem)
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve file extended properties")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file_item = ctx.web.get_file_by_server_relative_url(args.file_url).listItemAllFields.get().execute_query()
    for k, v in file_item.properties.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
