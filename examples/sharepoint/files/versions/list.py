"""
Retrieves versions of the file
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve versions of a file")
    parser.add_argument("--file-url", default="SitePages/Home.aspx", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file_with_versions = (
        ctx.web.get_file_by_server_relative_path(args.file_url).expand(["Versions"]).get().execute_query()
    )

    for version in file_with_versions.versions:
        # print(version.properties.get("Created"))
        print(version.version_label)


if __name__ == "__main__":
    main()
