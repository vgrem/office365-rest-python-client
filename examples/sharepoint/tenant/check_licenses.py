"""
Checks whether the tenant has an Intune license.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Check whether the tenant has an Intune license").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = admin_client.tenant.check_tenant_intune_license().execute_query()
    print(f"Intune license: {'Yes' if result.value else 'No'}")


if __name__ == "__main__":
    main()
