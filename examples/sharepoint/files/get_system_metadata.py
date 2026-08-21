"""
Retrieves file system metadata
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve file system metadata")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file = (
        ctx.web.get_file_by_server_relative_url(args.file_url)
        .expand(["ModifiedBy", "Author", "TimeCreated", "TimeLastModified"])
        .get()
        .execute_query()
    )

    print(file.author)
    print(file.modified_by)
    print(file.time_created)
    print(file.time_last_modified)


if __name__ == "__main__":
    main()
