"""
Retrieves file extended properties (accessible via associated ListItem)
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve file extended properties")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file_item = ctx.web.get_file_by_server_relative_url(args.file_url).listItemAllFields.get().execute_query()
    for k, v in file_item.properties.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
