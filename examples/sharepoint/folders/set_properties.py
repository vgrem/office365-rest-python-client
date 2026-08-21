"""
Demonstrates how to update folder properties.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/folder-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Updates folder properties")
    parser.add_argument("--folder-url", default="Shared Documents/Archive", help="folder url")
    parser.add_argument("--prop-name", default="DocScope", help="property name")
    parser.add_argument("--prop-value", default="Public", help="property value")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    folder = ctx.web.get_folder_by_server_relative_path(args.folder_url)
    folder_item = folder.list_item_all_fields
    folder_item.set_property(args.prop_name, args.prop_value).update().execute_query()


if __name__ == "__main__":
    main()
