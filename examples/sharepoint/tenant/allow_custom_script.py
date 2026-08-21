"""
Allow or prevent custom script

As a Global Administrator or SharePoint Administrator in Microsoft 365, you can allow custom script as a way
of letting users change the look, feel, and behavior of sites and pages to meet organizational objectives or
individual needs. If you allow custom script, all users who have "Add and Customize Pages" permission to a site
or page can add any script they want.
(By default, users who create sites are site owners and therefore have this permission.)

Demonstrates how to determine whether custom script on SharePoint site is enabled and enable  it if disabled

https://learn.microsoft.com/en-us/sharepoint/allow-or-prevent-custom-script
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.deny_add_and_customize_pages_status import (
    DenyAddAndCustomizePagesStatus,
)
from tests.settings import admin_site_url, client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Allow or prevent custom script on a site")
    parser.add_argument("--site-url", default=team_site_url, help="Site URL to configure")
    args = parser.parse_args()

    admin_client = ClientContext(admin_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    site_props = admin_client.tenant.get_site_properties_by_url(args.site_url, True).execute_query()
    if site_props.deny_add_and_customize_pages == DenyAddAndCustomizePagesStatus.Disabled:
        print(f"Enabling custom script on site: {args.site_url}...")
        site_props.deny_add_and_customize_pages = DenyAddAndCustomizePagesStatus.Enabled
        site_props.update().execute_query()
        print("[Ok] Updated")
    elif site_props.deny_add_and_customize_pages == DenyAddAndCustomizePagesStatus.Enabled:
        print(f"[Skipping] Custom script has already been allowed on site: {args.site_url}")
    else:
        print("Unknown status detected")


if __name__ == "__main__":
    main()
