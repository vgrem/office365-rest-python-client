"""
Exports tenant settings to a CSV file in the Style Library.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Export tenant settings to a CSV file").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = admin_client.tenant.export_to_csv(view_xml="<View/>", list_name="Style Library").execute_query()
    print("Sites details have been exported into {0}{1}".format(admin_site_url, result.value))


if __name__ == "__main__":
    main()
