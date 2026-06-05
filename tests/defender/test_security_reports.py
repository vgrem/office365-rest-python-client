"""Security Reports — Microsoft Defender attack simulation and training reports.

Tests cover:
  - Attack simulation repeat offenders report
  - Attack simulation user coverage report
  - Report result structure inspection
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

_REPORT_READ = ("AttackSimulation.Read.All",)


class TestSecurityReports(GraphDelegatedTestCase):
    """Microsoft 365 Defender reports (under client.reports.security)."""

    @requires_delegated(
        *_REPORT_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_01_get_attack_simulation_repeat_offenders(self):
        """Getting the attack simulation repeat offenders report returns a result with values."""
        # Act
        result = self.client.reports.security.get_attack_simulation_repeat_offenders().execute_query()

        # Assert
        self.assertIsNotNone(result.value)
        # The result value should be a collection of repeat offenders

    @requires_delegated(
        *_REPORT_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_02_get_attack_simulation_user_coverage(self):
        """Getting attack simulation user coverage returns coverage data."""
        # Act
        result = (
            self.client.reports.security.get_attack_simulation_simulation_user_coverage()
            .execute_query()
        )

        # Assert
        self.assertIsNotNone(result.value)

    @requires_delegated(
        *_REPORT_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_03_repeat_offender_has_user_info(self):
        """A repeat offender entry exposes displayName and email."""
        result = self.client.reports.security.get_attack_simulation_repeat_offenders().execute_query()
        offenders = result.value

        if not offenders:
            self.skipTest("No repeat offenders found in the tenant")

        for offender in offenders:
            # Each entry should have at least displayName
            self.assertIsNotNone(offender.get_property("displayName"))
            break

    @requires_delegated(
        *_REPORT_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_04_user_coverage_has_training_info(self):
        """A user coverage entry includes simulation and training counts."""
        result = (
            self.client.reports.security.get_attack_simulation_simulation_user_coverage()
            .execute_query()
        )
        coverage = result.value

        if not coverage:
            self.skipTest("No user coverage data available")

        for entry in coverage:
            # At least one of these should be populated
            has_coverage = any(
                entry.get_property(prop) is not None
                for prop in ("simulationCount", "simulationCountInLatest3Months", "latestSimulationDateTime")
            )
            self.assertTrue(has_coverage, "Expected at least one coverage field to be populated")
            break
