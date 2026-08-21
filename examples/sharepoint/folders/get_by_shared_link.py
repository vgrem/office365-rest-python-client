"""
Returns a folder object from a tokenized sharing link URL.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.links.kind import SharingLinkKind
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Gets a folder from a sharing link URL")
    parser.add_argument("--folder-url", default="Shared Documents/Archive", help="folder url")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.get_folder_by_server_relative_url(args.folder_url)
    # Share a folder
    result = folder.share_link(SharingLinkKind.OrganizationView).execute_query()

    shared_folder = ctx.web.get_folder_by_guest_url(str(result.value)).execute_query()
    print(shared_folder)


if __name__ == "__main__":
    main()
