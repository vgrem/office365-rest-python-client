"""
SharePoint and OneDrive tenant settings report (with optional updates).

Maps to the admin center "SharePoint settings" page.

Requires delegated permission ``SharePointTenantSettings.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/sharepointsettings-get
"""

import argparse

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="SharePoint tenant settings")
    parser.add_argument("--set-legacy-auth", choices=["on", "off"], help="Enable/disable legacy auth protocols")
    parser.add_argument("--set-page-commenting", choices=["on", "off"], help="Enable/disable commenting on pages")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    settings = client.admin.sharepoint.settings

    if args.set_legacy_auth or args.set_page_commenting:
        if args.set_legacy_auth:
            settings.set_property("isLegacyAuthProtocolsEnabled", args.set_legacy_auth == "on")
        if args.set_page_commenting:
            settings.set_property("isCommentingOnSitePagesEnabled", args.set_page_commenting == "on")
        settings.update().execute_query()
        print("SharePoint settings updated.\n")

    settings.get().execute_query()
    idle = settings.idle_session_sign_out
    print("SharePoint and OneDrive tenant settings:")
    print(f"  Sharing capability:      {settings.sharing_capability}")
    print(f"  Sharing domain mode:     {settings.sharing_domain_restriction_mode}")
    print(f"  Allowed domains:         {', '.join(settings.sharing_allowed_domain_list or []) or '-'}")
    print(f"  Blocked domains:         {', '.join(settings.sharing_blocked_domain_list or []) or '-'}")
    print(
        f"  Idle session sign-out:   enabled={idle.isEnabled if idle else '?'}"
        f"  warn after={idle.warnAfterInSeconds if idle else '?'}s"
        f"  sign out after={idle.signOutAfterInSeconds if idle else '?'}s"
    )
    print(f"  Legacy auth protocols:   {settings.is_legacy_auth_protocols_enabled}")
    print(f"  Commenting on pages:     {settings.is_commenting_on_site_pages_enabled}")
    print(f"  Default managed path:    {settings.site_creation_default_managed_path}")
    print(f"  Default storage limit:   {settings.site_creation_default_storage_limit_in_mb} MB")


if __name__ == "__main__":
    main()
