"""
Get the teams in Microsoft Teams that the current user is a direct member of
"""

import json

from office365.sharepoint.client_context import ClientContext
from tests import test_client_id, test_password, test_team_site_url, test_tenant, test_username

ctx = ClientContext(test_team_site_url).with_username_and_password(
    test_tenant, test_client_id, test_username, test_password
)
result = ctx.group_site_manager.get_current_user_joined_teams().execute_query()
data = json.loads(result.value)
for item in data["value"]:
    print(item["displayName"])
