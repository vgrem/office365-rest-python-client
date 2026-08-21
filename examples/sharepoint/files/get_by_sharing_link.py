"""
Gets file by shared link
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get a file by a sharing link")
    parser.add_argument(
        "--file-url",
        default="/sites/team/SitePages/How To Use This Library.aspx",
        help="server-relative file URL",
    )
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    # Generate sharing link url for a file first
    file = ctx.web.get_file_by_server_relative_url(args.file_url)
    # Share a file
    result = file.share_link(SharingLinkKind.OrganizationView).execute_query()

    # Resolve file by sharing link url (guest url)
    file = ctx.web.get_file_by_guest_url(str(result.value)).execute_query()
    print(file)


if __name__ == "__main__":
    main()
