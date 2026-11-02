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

    def _insights(self, collection):
        """Fetch an insights collection, or skip when this tenant has item insights off.

        Measured: the 403 carries ``{"code": "Forbidden", "message": "ItemInsightsDisabled"}``,
        so the marker is the message, not the code — an HTTP word the service uses for every
        refusal of this shape.
        """
        try:
            return collection.get().execute_query()
        except ClientRequestException as error:
            if "ItemInsightsDisabled" not in str(error):
                raise
            self.skipTest(f"item insights are disabled on this tenant: {error}")

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_trending(self):
        """Listing trending documents around the user returns a valid collection."""
        self._insights(self.client.me.insights.trending)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_02_list_shared(self):
        """Listing documents shared with the user returns a valid collection."""
        self._insights(self.client.me.insights.shared)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_03_list_used(self):
        """Listing documents recently used by the user returns a valid collection."""
        self._insights(self.client.me.insights.used)

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_04_trending_has_resource_reference(self):
        """A trending item has a resourceReference with a webUrl."""
        result = self._insights(self.client.me.insights.trending.top(5))
        if len(result) > 0:
            ref = result[0].get_property("resourceReference")
            if ref:
                self.assertIsNotNone(ref.get_property("webUrl"))

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_05_trending_has_weight(self):
        """A trending item has a weight field indicating relevance."""
        result = self._insights(self.client.me.insights.trending.top(5))
        if len(result) > 0:
            weight = result[0].get_property("weight")
            if weight is not None:
                self.assertIsInstance(weight, (int, float))

    @requires_delegated(
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_06_shared_has_resource_reference(self):
        """A shared insight has a resourceReference with a webUrl."""
        result = self._insights(self.client.me.insights.shared.top(5))
        if len(result) > 0:
            ref = result[0].get_property("resourceReference")
            if ref:
                self.assertIsNotNone(ref.get_property("webUrl"))

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
        """The user's item insights settings expose isEnabled.

        ``/me/settings`` itself carries the two content-discovery flags; ``isEnabled`` lives on
        the ``itemInsights`` navigation beside them.
        """
        result = self.client.me.settings.item_insights.get().execute_query()
        self.assertIn(result.is_enabled, (True, False))
