"""
Get audit settings for a SharePoint site.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/csom/audit
"""

import argparse

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Get audit settings for a SharePoint site").parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant,
        client_id=client_id,
        username=username,
        password=password,
    )
    audit = ctx.site.audit.get().execute_query()
    print(f"Allow designer: {audit.allow_designer}")


if __name__ == "__main__":
    main()
