"""
Retrieves detailed properties for a specific SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Retrieve detailed properties for a SharePoint site")
    parser.add_argument("--site-url", default=team_site_url, help="Site URL to retrieve")
    args = parser.parse_args()

    client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site_props = client.tenant.get_site_properties_by_url(args.site_url, True).execute_query()
    print(site_props)


if __name__ == "__main__":
    main()
