"""
Get recently modified files from the current user's recent file list.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get recent files for the current user")
    parser.add_argument("--top", type=int, default=100, help="number of recent files (default 100)")
    args = parser.parse_args()

    ctx = ClientContext(site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.web.current_user.get_recent_files(args.top).execute_query()
    files = json.loads(result.value)
    print(f"Recent files ({len(files)}):")
    for item in files:
        print(f"  {item.get('Name', '?')}  ({item.get('ServerRelativeUrl', item.get('Url', '?'))})")


if __name__ == "__main__":
    main()
