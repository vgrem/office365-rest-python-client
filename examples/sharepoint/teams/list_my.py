"""
Gets the Microsoft Teams that the current user is a direct member of.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="List Teams the current user is a direct member of")
    parser.add_argument("--site-url", default=team_site_url, help="target site URL")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.group_site_manager.get_current_user_joined_teams().execute_query()
    data = json.loads(result.value)
    for item in data["value"]:
        print(item["displayName"])


if __name__ == "__main__":
    main()
