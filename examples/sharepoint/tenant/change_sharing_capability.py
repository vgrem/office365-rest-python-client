"""
Set external sharing on site collections in Office 365

https://learn.microsoft.com/en-us/sharepoint/dev/solution-guidance/set-external-sharing-on-site-collections-in-office-365
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.sharing_capabilities import (
    SharingCapabilities,
)
from tests.settings import admin_site_url, client_id, client_secret, team_site_url, tenant


def main():
    parser = argparse.ArgumentParser(description="Set external sharing on site collections")
    parser.add_argument("--site-url", default=team_site_url, help="Site URL to configure")
    args = parser.parse_args()

    admin_client = ClientContext(admin_site_url).with_client_secret(tenant, client_id, client_secret)

    site_props = admin_client.tenant.get_site_properties_by_url(args.site_url).execute_query()

    site_props.sharing_capability = SharingCapabilities.ExternalUserAndGuestSharing
    site_props.update().execute_query()


if __name__ == "__main__":
    main()
