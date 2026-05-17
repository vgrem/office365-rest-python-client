from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.teams.channel_manager import TeamChannelManager

from tests import (
    test_client_id,
    test_password,
    test_team_site_url,
    test_tenant,
    test_username,
)
from tests.sharepoint.sharepoint_case import SPTestCase


class TestTeam(SPTestCase):
    def test1_get_team_site_data(self):
        return_type = TeamChannelManager.get_team_site_data(self.client).execute_query()
        self.assertIsNotNone(return_type.properties.get("SiteUrl"))

    def test2_get_current_user_joined_teams(self):
        my_client = ClientContext(test_team_site_url).with_username_and_password(
            test_tenant, test_client_id, test_username, test_password
        )
        result = my_client.group_site_manager.get_current_user_joined_teams().execute_query()
        self.assertIsNotNone(result.value)

    def test3_recent_and_joined_teams(self):
        result = self.client.group_site_manager.recent_and_joined_teams().execute_query()
        self.assertIsNotNone(result.value)

    def test4_get_current_user_shared_channel_member_groups(self):
        result = self.client.group_site_manager.get_current_user_shared_channel_member_groups().execute_query()
        self.assertIsNotNone(result.value)
