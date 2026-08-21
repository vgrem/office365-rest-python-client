"""
Connect to SharePoint using browser-session cookies (FedAuth / rtFa).

This is useful when you already have authenticated browser cookies
(e.g. from Playwright, Selenium, or a logged-in browser session).
Cookie values are passed as a dict; for capturing from a real browser
see examples/sharepoint/auth_cookies.py (uses Playwright storage state).

See https://learn.microsoft.com/en-us/sharepoint/dev/apis/sharepoint-rest-api
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import site_url


def main():
    argparse.ArgumentParser(description="Connect to SharePoint using browser-session cookies").parse_args()

    cookies = {"FedAuth": "...", "rtFa": "...", "SPOIDCRL": "..."}

    ctx = ClientContext(site_url).with_cookies(lambda: cookies)
    web = ctx.web.get().execute_query()
    print(web.url)


if __name__ == "__main__":
    main()
