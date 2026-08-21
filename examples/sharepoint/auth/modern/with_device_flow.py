"""
Connect to SharePoint using device code flow.

Useful for devices or environments without a web browser.
The user authenticates on another device by visiting a URL
and entering the displayed code.

See https://learn.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, site_url, tenant


def main():
    argparse.ArgumentParser(description="Connect to SharePoint using device code flow").parse_args()

    ctx = ClientContext(site_url).with_device_flow(tenant, client_id)
    me = ctx.web.current_user.get().execute_query()
    print(me.login_name)
    web = ctx.web.get().execute_query()
    print(web.title)


if __name__ == "__main__":
    main()
