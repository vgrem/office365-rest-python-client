"""Tests for Microsoft Graph Insights API."""

from office365.runtime.client_request_exception import ClientRequestException

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestInsights(GraphDelegatedTestCase):
    """Tests for Microsoft Graph Insights API (trending, shared, used)."""

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test1_list_trending(self):
        """List trending documents around the user."""
        try:
            result = self.client.me.insights.trending.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test2_list_shared(self):
        """List documents shared with the user."""
        try:
            result = self.client.me.insights.shared.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test3_list_used(self):
        """List documents recently used by the user."""
        try:
            result = self.client.me.insights.used.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test4_get_user_settings(self):
        """Get user settings."""
        result = self.client.me.settings.get().execute_query()
        self.assertIsNotNone(result.resource_path)
