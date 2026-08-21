"""
Retrieves all SharePoint sites from a tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Retrieve all SharePoint sites from a tenant").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    tenant_obj = Tenant(admin_client)
    result = tenant_obj.get_site_properties_from_sharepoint_by_filters("").execute_query()
    i = 0
    for siteProps in result:
        print(f"({i} of {len(result)}) {siteProps.url}")
        i += 1


if __name__ == "__main__":
    main()
