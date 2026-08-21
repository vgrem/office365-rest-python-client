"""
Since for new tenants, apps using an ACS app-only access token is disabled by default,
you can change the behavior using the below script.

NOTE: ACS app-only authentication is deprecated — use Microsoft Entra app-only
(client certificate or client secret) instead.

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/security-apponly-azureacs
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import admin_site_url, client_id, password, tenant, username


def main():
    argparse.ArgumentParser(description="Enable ACS app-only authentication on the tenant").parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    if admin_client.tenant.get_property("DisableCustomAppAuthentication"):
        print("Enabling ACS app-only access token auth on tenant...")
        admin_client.tenant.set_property("DisableCustomAppAuthentication", False).update().execute_query()
        print("Done")
    else:
        print("ACS app-only access token auth has been already enabled on tenant")


if __name__ == "__main__":
    main()
