"""
Get the personal (OneDrive) site for the current user.

Any authenticated user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Get the personal (OneDrive) site for the current user").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    my_site = ctx.web.current_user.get_personal_site().execute_query()
    print(f"Personal site: {my_site.url}")


if __name__ == "__main__":
    main()
