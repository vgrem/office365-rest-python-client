"""
Demonstrates how to determine whether a user has permissions for a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.permissions.kind import PermissionKind
from tests.settings import client_id, password, site_url, tenant, user_principal_alt, username


def main():
    parser = argparse.ArgumentParser(description="Determine whether a user has permissions for a file")
    parser.add_argument("--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative file URL")
    args = parser.parse_args()

    client = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    target_user = client.web.site_users.get_by_email(user_principal_alt)
    target_file = client.web.get_file_by_server_relative_path(args.file_url)
    result = target_file.get_user_effective_permissions(target_user).execute_query()
    # verify whether user has Reader role to a file
    if result.value.has(PermissionKind.OpenItems):
        print("User has access to read a file")


if __name__ == "__main__":
    main()
