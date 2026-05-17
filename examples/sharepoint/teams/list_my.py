"""
Gets the Microsoft Teams that the current user is a direct member of.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/rest-api/navigation/team-operations
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
