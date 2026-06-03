"""
Get channels in a Microsoft Team.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
"""

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
team_id = "your-team-id"

result = ctx.group_site_manager.get_team_channels(team_id).execute_query()
for channel in result.value.value:
    print(f"  {channel.displayName}  ({channel.id})")
