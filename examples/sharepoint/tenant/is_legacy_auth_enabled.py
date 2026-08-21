"""
Checks whether legacy authentication protocols are enabled on the tenant.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/tenant-operations
"""

import argparse
from pprint import pprint

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Check whether legacy authentication protocols are enabled").parse_args()

    tenant_obj = Tenant.from_url(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )

    details = tenant_obj.get().execute_query()
    pprint(details.legacy_auth_protocols_enabled)


if __name__ == "__main__":
    main()
