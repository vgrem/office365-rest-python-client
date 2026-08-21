"""
Retrieves and prints the effective permission levels for a user on a file.

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/file-operations
"""

import argparse
from pprint import pprint

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, user_principal_alt, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve effective permission levels for a user on a file")
    parser.add_argument("--file-url", default="Shared Documents/Financial Sample.xlsx", help="server-relative file URL")
    args = parser.parse_args()

    client = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    target_user = client.web.site_users.get_by_email(user_principal_alt)
    target_file = client.web.get_file_by_server_relative_path(args.file_url)
    result = target_file.get_user_effective_permissions(target_user).execute_query()
    pprint(result.value.permission_levels)  # print all permission levels


if __name__ == "__main__":
    main()
