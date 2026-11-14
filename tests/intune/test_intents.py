"""Intents: the template-driven policy generation that replaced "one profile per setting".

``deviceManagement/intents`` exists on ``beta`` only - ``v1.0`` refuses the *member* before the
request is sent, which ``test_versions.py`` pins - so these reads address the beta client.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestIntents(GraphDelegatedTestCase):
    """The intent family: the policy, its settings, and its aggregated state."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_01_intents_are_listed(self):
        """``/deviceManagement/intents`` answers with a collection."""
        intents = self.client_beta.device_management.intents
        self.assertTrue(str(intents.resource_path).endswith("/intents"))

        intents.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_02_an_intent_is_built_from_categories_of_settings(self):
        """An intent's settings are grouped into categories, and read as their own collection."""
        rows = self.client_beta.device_management.intents.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no device management intent")
        intent = rows[0]

        categories = intent.settings.top(5).get().execute_query()

        self.assertIn(f"/intents/{intent.id}/settings", str(categories.resource_path))

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_03_an_intent_aggregates_its_device_state(self):
        """``deviceStateSummary`` is the intent's roll-up: one object, not one row per device."""
        rows = self.client_beta.device_management.intents.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no device management intent")
        intent = rows[0]

        summary = intent.device_state_summary

        self.assertIsInstance(summary.get().execute_query(), type(summary))
