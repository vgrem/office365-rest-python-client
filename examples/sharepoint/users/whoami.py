"""
Show the current SharePoint user (title, login, UPN, email).

Any authenticated user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/user-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Show the current SharePoint user").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    me = ctx.web.current_user.get().execute_query()
    print(f"Title:     {me.title}")
    print(f"Login:     {me.login_name}")
    print(f"UPN:       {me.user_principal_name}")
    print(f"Email:     {me.email}")


if __name__ == "__main__":
    main()
