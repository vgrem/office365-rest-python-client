"""
Retrieves the home sites configured in the SharePoint tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Retrieve the home sites configured in the SharePoint tenant").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = admin_client.tenant.get_home_sites().execute_query()
    for details in result.value:
        print(f" {details.Url}")


if __name__ == "__main__":
    main()
