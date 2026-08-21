"""
Retrieves versions of the file
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, client_secret, site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Retrieve versions of a file")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)
    file_with_versions = (
        ctx.web.get_file_by_server_relative_path(args.file_url).expand(["Versions"]).get().execute_query()
    )

    for version in file_with_versions.versions:
        # print(version.properties.get("Created"))
        print(version.version_label)


if __name__ == "__main__":
    main()
