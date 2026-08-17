"""
Gets primary and secondary site collection administrators for a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, cert_path, cert_thumbprint, client_id, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Get site collection administrators")
    parser.add_argument("--site-url", default=team_site_url, help="Site URL to inspect")
    args = parser.parse_args()

    tenant_obj = Tenant.from_url(admin_site_url).with_client_certificate(
        tenant, client_id=client_id, thumbprint=cert_thumbprint, cert_path=cert_path
    )

    print("Primary Administrators:")
    result = tenant_obj.get_site_administrators_by_site_url(args.site_url).execute_query()
    for admin in result.value:
        print(f"  {admin.loginName}")

    print("\nSecondary Administrators:")
    result = tenant_obj.get_site_secondary_administrators_by_site_url(args.site_url).execute_query()
    for admin in result.value:
        print(f"  {admin.loginName}")


if __name__ == "__main__":
    main()
