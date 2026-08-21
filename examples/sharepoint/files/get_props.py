"""
Retrieves basic file properties
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve basic file properties")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file = ctx.web.get_file_by_server_relative_url(args.file_url).get().execute_query()

    print("File size: ", file.length)
    print("File name: ", file.name)
    print("File url: ", file.server_relative_url)


if __name__ == "__main__":
    main()
