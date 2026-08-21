"""
Demonstrates how to assign custom permissions on a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.sharing.role_type import RoleType
from tests.settings import client_id, client_secret, site_url, tenant, user_principal


def main():
    parser = argparse.ArgumentParser(description="Assign custom permissions on a file")
    parser.add_argument("--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative file URL")
    args = parser.parse_args()

    client = ClientContext(site_url).with_client_secret(tenant, client_id, client_secret)

    role_def = client.web.role_definitions.get_by_type(RoleType.Contributor)
    user = client.web.site_users.get_by_principal_name(user_principal)
    target_file = client.web.get_file_by_server_relative_path(args.file_url)

    # assign a custom permissions for the user to a file
    target_file.listItemAllFields.add_role_assignment(user, role_def).execute_query()


if __name__ == "__main__":
    main()
