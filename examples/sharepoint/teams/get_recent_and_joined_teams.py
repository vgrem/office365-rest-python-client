"""
Get recent and joined teams for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
"""

import argparse
import json

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    argparse.ArgumentParser(description="Get joined teams for the current user").parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.group_site_manager.recent_and_joined_teams(
        include_recent=True, include_teams=True, include_pinned=True
    ).execute_query()
    joined = result.value.joinedTeams or "{}"
    data = json.loads(joined)
    teams = data.get("value", []) if isinstance(data, dict) else []
    print(f"Joined teams ({len(teams)}):")
    for item in teams:
        print(f"  {item.get('displayName', '?')}  ({item.get('id', '?')})")


if __name__ == "__main__":
    main()
