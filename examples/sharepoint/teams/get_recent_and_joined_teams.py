"""
Get recent and joined teams for the current user.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
"""

import json

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
result = ctx.group_site_manager.recent_and_joined_teams(
    include_recent=True, include_teams=True, include_pinned=True
).execute_query()
data = json.loads(result.value.joined_teams)
for item in data.get("value", []):
    print(f"  {item.get('displayName', '')}  ({item.get('id', '')})")
