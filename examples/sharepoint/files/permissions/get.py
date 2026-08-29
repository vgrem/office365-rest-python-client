"""
Retrieves the permissions on the file that are assigned to the current user.
"""

import argparse
from pprint import pprint

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve permissions on a file for the current user")
    parser.add_argument("--file-url", default="Shared Documents/big_buck_bunny.mp4", help="server-relative file URL")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    file = ctx.web.get_file_by_server_relative_url(args.file_url)
    file_item = file.listItemAllFields.select(["EffectiveBasePermissions"]).get().execute_query()
    pprint(file_item.effective_base_permissions.permission_levels)


if __name__ == "__main__":
    main()
