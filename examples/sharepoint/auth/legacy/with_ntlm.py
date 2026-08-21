"""
Connect to SharePoint on-premises using NTLM authentication.

This method is only relevant for SharePoint on-premises deployments.
"""

import argparse
import logging

from office365.sharepoint.client_context import ClientContext
from tests.settings import password, team_site_url, username


def main():
    argparse.ArgumentParser(description="Connect to SharePoint on-premises with NTLM").parse_args()

    logging.basicConfig(level=logging.DEBUG)

    ctx = ClientContext(team_site_url, allow_ntlm=True).with_user_credentials(username, password)
    web = ctx.web.get().execute_query()
    print(web.url)


if __name__ == "__main__":
    main()
