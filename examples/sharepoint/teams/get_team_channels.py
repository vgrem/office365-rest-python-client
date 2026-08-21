"""
Get channels in a Microsoft Team.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
"""

import argparse
import json
import sys

from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Get channels in a Microsoft Team")
    parser.add_argument("--team-id", required=True, help="team (group) id")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    result = ctx.group_site_manager.get_team_channels(args.team_id).execute_query()
    data = json.loads(result.value)
    channels = data.get("value", []) if isinstance(data, dict) else []
    if not channels:
        sys.exit("No channels found.")
    for channel in channels:
        print(f"  {channel.get('displayName', '?')}  ({channel.get('id', '?')})")


if __name__ == "__main__":
    main()
