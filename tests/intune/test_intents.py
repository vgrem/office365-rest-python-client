"""Intents: the template-driven policy generation that replaced "one profile per setting".

``deviceManagement/intents`` exists on ``beta`` only - ``v1.0`` refuses the *member* before the
request is sent, which ``test_versions.py`` pins - so these reads address ``self.dm_beta``.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, IntuneCase


class TestIntents(IntuneCase):
    """The intent family: the policy, its settings, and its aggregated state."""

    @requires_delegated(*CONFIGURATION)
    def test_01_intents_are_listed(self):
        """``/deviceManagement/intents`` answers with a collection."""
        self.read(self.dm_beta.intents, "intents")

    @requires_delegated(*CONFIGURATION)
    def test_02_an_intent_is_built_from_categories_of_settings(self):
        """An intent's settings are grouped into categories, and read as their own collection."""
        intents = self.read(self.dm_beta.intents, "intents")
        intent = self.row_or_skip(intents, "device management intent")
        categories = intent.settings.top(5).get().execute_query()

        self.assertIn(f"/intents/{intent.id}/settings", str(categories.resource_path))

    @requires_delegated(*CONFIGURATION)
    def test_03_an_intent_aggregates_its_device_state(self):
        """``deviceStateSummary`` is the intent's roll-up: one object, not one row per device."""
        intents = self.read(self.dm_beta.intents, "intents")
        intent = self.row_or_skip(intents, "device management intent")

        summary = intent.device_state_summary

        self.assertIsInstance(summary.get().execute_query(), type(summary))
