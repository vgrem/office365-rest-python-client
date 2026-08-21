"""
Prints SharePoint server settings including SharePoint Online status and installed languages.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/server-operations
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.server_settings import ServerSettings
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Print SharePoint server settings").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    is_online = ServerSettings.is_sharepoint_online(ctx)
    blocked_file_extensions = ServerSettings.get_blocked_file_extensions(ctx)
    installed_languages = ServerSettings.get_global_installed_languages(ctx, 15)
    ctx.execute_batch()
    print(f"Is SharePoint Online? : {is_online.value}")
    print(f"Blocked file extensions : {len(blocked_file_extensions.value)}")
    print(f"Installed languages : {installed_languages}")


if __name__ == "__main__":
    main()
