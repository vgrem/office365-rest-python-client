"""
Retrieves SharePoint sites that are not associated with a Microsoft 365 group.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Find SharePoint sites without a Microsoft 365 group").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    tenant_obj = Tenant(admin_client)
    sites = tenant_obj.get_site_properties_from_sharepoint_by_filters("").execute_query()
    for site in sites:
        if site.get_property("GroupId") == "00000000-0000-0000-0000-000000000000":
            print(site.url)


if __name__ == "__main__":
    main()
