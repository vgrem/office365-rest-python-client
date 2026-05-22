"""Tests for Microsoft Graph Insights API."""

from unittest import skipIf

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestInsights(GraphDelegatedTestCase):
    """Tests for Microsoft Graph Insights API (trending, shared, used)."""

    insights_enabled = False

    def test0_if_insights_disabled(self):
        """Check if item insights are enabled for the user."""
        result = self.client.me.settings.item_insights.get().execute_query()
        self.assertIsNotNone(result.is_enabled)
        self.__class__.insights_enabled = result.is_enabled

    @skipIf(not insights_enabled, "Item insights are disabled")
    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test1_list_trending(self):
        """List trending documents around the user."""
        result = self.client.me.insights.trending.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test2_list_shared(self):
        """List documents shared with the user."""
        result = self.client.me.insights.shared.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("Sites.Read.All", "Sites.ReadWrite.All", or_roles=["Global Administrator"])
    def test3_list_used(self):
        """List documents recently used by the user."""
        result = self.client.me.insights.used.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("User.Read", "User.Read.All", "User.ReadWrite.All", or_roles=["Global Administrator"])
    def test4_get_user_settings(self):
        """Get user settings."""
        result = self.client.me.settings.get().execute_query()
        self.assertIsNotNone(result.resource_path)
