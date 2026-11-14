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
from tests.graph_case import GraphDelegatedTestCase

CONFIGURATION = (
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementConfiguration.ReadWrite.All",
)


class TestEndpointAnalytics(GraphDelegatedTestCase):
    """Scores, baselines and app health, all on the preview root."""

    @requires_delegated(*CONFIGURATION, require_licenses=["INTUNE_P2"])
    def test_01_device_performance_scores_are_listed(self):
        """A device score is per-device, so an empty collection is the normal answer here."""
        scores = self.client_beta.device_management.user_experience_analytics_device_performance
        self.assertTrue(str(scores.resource_path).endswith("/userExperienceAnalyticsDevicePerformance"))

        scores.top(5).get().execute_query()

    @requires_delegated(*CONFIGURATION, require_licenses=["INTUNE_P2"])
    def test_02_the_baselines_are_service_provided(self):
        """A baseline is Microsoft's reference, shipped with the licence, not with enrolment."""
        rows = self.client_beta.device_management.user_experience_analytics_baselines.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant ships no endpoint analytics baseline")

        self.assertIsNotNone(rows[0].get_property("displayName"))

    @requires_delegated(*CONFIGURATION, require_licenses=["INTUNE_P2"])
    def test_03_the_anomaly_family_is_a_collection_of_issues(self):
        """An anomaly is one detected issue with an asset, a severity and a device count.

        Measured to answer ``200`` on beta even on a tenant nobody enrolled: the service
        computes these from the fleet it can see, so the answer is a collection first and an
        issue second.
        """
        anomalies = self.client_beta.device_management.user_experience_analytics_anomaly
        self.assertTrue(str(anomalies.resource_path).endswith("/userExperienceAnalyticsAnomaly"))

        rows = anomalies.top(5).get().execute_query()

        self.assertIs(rows._item_type, UserExperienceAnalyticsAnomaly)
        if len(rows):
            self.assertIn(rows[0].get_property("severity"), list(UserExperienceAnalyticsAnomalySeverity))

    @requires_delegated(*CONFIGURATION, require_licenses=["INTUNE_P2"])
    def test_04_battery_capacity_is_one_summary_not_a_collection(self):
        """`userExperienceAnalyticsBatteryHealthCapacityDetails` is a single navigation.

        The one-entity answer is the reason this family needed a getter and not a collection,
        and the entity type is what says the render got that right.
        """
        capacity = self.client_beta.device_management.user_experience_analytics_battery_health_capacity_details

        self.assertIsInstance(capacity, UserExperienceAnalyticsBatteryHealthCapacityDetails)
        self.assertTrue(
            str(capacity.resource_path).endswith("/deviceManagement/userExperienceAnalyticsBatteryHealthCapacityDetails")
        )
        self.assertIsInstance(capacity.get().execute_query(), UserExperienceAnalyticsBatteryHealthCapacityDetails)
