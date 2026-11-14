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

from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly import (
    UserExperienceAnalyticsAnomaly,
)
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_anomaly_severity import (
    UserExperienceAnalyticsAnomalySeverity,
)
from office365.intune.devices.management.userexperienceanalytics.user_experience_analytics_battery_health_capacity_details import (  # noqa: E501
    UserExperienceAnalyticsBatteryHealthCapacityDetails,
)

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

    @requires_delegated(*CONFIGURATION, require_licenses=list(ENDPOINT_ANALYTICS))
    def test_03_the_anomaly_family_is_a_collection_of_issues(self):
        """An anomaly is one detected issue with an asset, a severity and a device count.

        Measured to answer ``200`` on beta even on a tenant nobody enrolled: the service
        computes these from the fleet it can see, so the answer is a collection first and an
        issue second.
        """
        rows = self.read(self.dm_beta.user_experience_analytics_anomaly, "userExperienceAnalyticsAnomaly")

        self.assertIs(rows._item_type, UserExperienceAnalyticsAnomaly)
        if len(rows):
            self.assertIsInstance(rows[0], UserExperienceAnalyticsAnomaly)
            self.assertIn(rows[0].get_property("severity"), list(UserExperienceAnalyticsAnomalySeverity))

    @requires_delegated(*CONFIGURATION, require_licenses=list(ENDPOINT_ANALYTICS))
    def test_04_battery_capacity_is_one_summary_not_a_collection(self):
        """`userExperienceAnalyticsBatteryHealthCapacityDetails` is a single navigation.

        The one-entity answer is the reason this family needed a getter and not a collection,
        and the entity type is what says the render got that right.
        """
        capacity = self.dm_beta.user_experience_analytics_battery_health_capacity_details

        self.assertIsInstance(capacity, UserExperienceAnalyticsBatteryHealthCapacityDetails)
        self.assertTrue(
            str(capacity.resource_path).endswith("/deviceManagement/userExperienceAnalyticsBatteryHealthCapacityDetails")
        )
        result = capacity.get().execute_query()
        self.assertIsInstance(result, UserExperienceAnalyticsBatteryHealthCapacityDetails)
