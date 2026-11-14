"""Endpoint analytics: the one Intune capability the published tables tie to a licence.

Every other Intune read is gated by a scope, and a licence buys nothing: this tenant's
``INTUNE_A`` sits at ``PendingInput`` for the signed-in user while the Settings Catalog answers
``200``. Endpoint analytics is the exception - Microsoft documents it as an Intune Plan 2 (or
Intune Suite) capability, and the service plan that carries it here is ``INTUNE_P2``.

So the guard on this file is ``require_licenses``, not a scope: on a tenant that bought only
Plan 1 these tests skip *by licence*, which is a different fact from a missing grant, and the
two are never collapsed into one skip.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, ENDPOINT_ANALYTICS, IntuneCase


class TestEndpointAnalytics(IntuneCase):
    """Scores, baselines and app health, all on the preview root."""

    @requires_delegated(*CONFIGURATION, require_licenses=list(ENDPOINT_ANALYTICS))
    def test_01_device_performance_scores_are_listed(self):
        """A device score is per-device, so an empty collection is the normal answer here."""
        self.read(
            self.dm_beta.user_experience_analytics_device_performance,
            "userExperienceAnalyticsDevicePerformance",
        )

    @requires_delegated(*CONFIGURATION, require_licenses=list(ENDPOINT_ANALYTICS))
    def test_02_the_baselines_are_service_provided(self):
        """A baseline is Microsoft's reference, shipped with the licence, not with enrolment."""
        baselines = self.read(self.dm_beta.user_experience_analytics_baselines, "userExperienceAnalyticsBaselines")
        baseline = self.row_or_skip(baselines, "endpoint analytics baseline")

        self.assertIsNotNone(baseline.get_property("displayName"))
