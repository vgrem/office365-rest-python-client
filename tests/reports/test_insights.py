"""Office Graph Insights — trending documents, shared, and recently used.

Tests cover:
  - Listing trending documents around the user
  - Listing documents shared with the user
  - Listing documents recently used by the user
  - Trending item property assertions (weight, resourceReference)
  - User insights settings (isEnabled)
  - Graceful skip when ItemInsightsDisabled
"""

from __future__ import annotations

from office365.runtime.client_request_exception import ClientRequestException

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestInsights(GraphDelegatedTestCase):
    """Office Graph Insights — trending, shared, and used items."""

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_trending(self):
        """Listing trending documents around the user returns a valid collection."""
        try:
            result = self.client.me.insights.trending.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_02_list_shared(self):
        """Listing documents shared with the user returns a valid collection."""
        try:
            result = self.client.me.insights.shared.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_03_list_used(self):
        """Listing documents recently used by the user returns a valid collection."""
        try:
            result = self.client.me.insights.used.get().execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_04_trending_has_resource_reference(self):
        """A trending item has a resourceReference with a webUrl."""
        try:
            result = self.client.me.insights.trending.top(5).get().execute_query()
            if len(result) > 0:
                ref = result[0].get_property("resourceReference")
                if ref:
                    self.assertIsNotNone(ref.get_property("webUrl"))
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_05_trending_has_weight(self):
        """A trending item has a weight field indicating relevance."""
        try:
            result = self.client.me.insights.trending.top(5).get().execute_query()
            if len(result) > 0:
                weight = result[0].get_property("weight")
                if weight is not None:
                    self.assertIsInstance(weight, (int, float))
        except ClientRequestException as e:
            if e.code == "ItemInsightsDisabled":
                self.skipTest("Item insights are disabled")
            raise

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_06_shared_has_resource_reference(self):
        """A shared insight has a resourceReference with a webUrl."""
        try:
            result = self.client.me.insights.shared.top(5).get().execute_query()
            if len(result) > 0:
                ref = result[0].get_property("resourceReference")
                if ref:
                    self.assertIsNotNone(ref.get_property("webUrl"))
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
    def test_07_get_user_settings(self):
        """Getting user settings returns a valid settings object."""
        result = self.client.me.settings.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "User.Read",
        "User.Read.All",
        "User.ReadWrite.All",
        bypass_roles=["User Administrator", "Global Reader", "Global Administrator"],
    )
    def test_08_user_settings_has_is_enabled(self):
        """User settings should expose an isEnabled field."""
        result = self.client.me.settings.get().execute_query()
        is_enabled = result.get_property("isEnabled")
        # Default is True; could be False if disabled
        self.assertIn(is_enabled, (True, False))
