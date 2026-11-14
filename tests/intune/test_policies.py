"""Policies: what the tenant enforces, on the settings the service actually ships.

Two generations live side by side. ``deviceConfigurations`` and ``deviceCompliancePolicies`` are
the classic profiles and exist on ``v1.0``; ``configurationPolicies`` is the Settings Catalog and
exists on ``beta`` only, where ``compliancePolicies`` mirrors it for compliance. A suite that
means the settings catalog has to say so by naming the beta client.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestClassicPolicies(GraphDelegatedTestCase):
    """The profiles the stable root carries."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_01_device_configurations_are_listed(self):
        """A configuration profile is addressed by ``/deviceConfigurations``."""
        profiles = self.client.device_management.device_configurations
        self.assertTrue(str(profiles.resource_path).endswith("/deviceConfigurations"))

        profiles.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_02_a_profile_names_its_platform(self):
        """One collection carries every platform, and ``@odata.type`` says which one a row is."""
        rows = self.client.device_management.device_configurations.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no configuration profile")

        profile = rows[0]
        self.assertIsNotNone(profile.get_property("displayName"))
        self.assertIsNotNone(profile.get_property("@odata.type"))

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_03_compliance_policies_are_listed(self):
        """Compliance policies are a separate family from configuration profiles."""
        policies = self.client.device_management.device_compliance_policies
        self.assertTrue(str(policies.resource_path).endswith("/deviceCompliancePolicies"))

        policies.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_04_a_compliance_policy_carries_its_assignments(self):
        """An assignment is a navigation off the policy, so an unassigned policy answers empty."""
        rows = self.client.device_management.device_compliance_policies.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no compliance policy")

        policy = rows[0]
        assignments = policy.assignments.top(5).get().execute_query()

        self.assertIn(f"/deviceCompliancePolicies/{policy.id}/assignments", str(assignments.resource_path))


class TestSettingsCatalog(GraphDelegatedTestCase):
    """The preview-root families that replaced the classic profiles."""

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_01_configuration_policies_are_listed(self):
        """``configurationPolicies`` is the Settings Catalog, and v1.0 has no such segment."""
        policies = self.client_beta.device_management.configuration_policies
        self.assertTrue(str(policies.resource_path).endswith("/configurationPolicies"))

        policies.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_02_the_catalog_ships_templates(self):
        """A template is a policy skeleton the tenant gets for free, so it needs no enrolment."""
        rows = self.client_beta.device_management.configuration_policy_templates.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant ships no settings catalog template")

        self.assertIsNotNone(rows[0].get_property("displayName"))

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_03_compliance_policies_are_listed_on_the_preview_root(self):
        """The catalog-era compliance family answers under ``compliancePolicies``."""
        policies = self.client_beta.device_management.compliance_policies
        self.assertTrue(str(policies.resource_path).endswith("/compliancePolicies"))

        policies.top(5).get().execute_query()

    @requires_delegated("DeviceManagementConfiguration.Read.All", "DeviceManagementConfiguration.ReadWrite.All")
    def test_04_assignment_filters_are_listed(self):
        """A filter is how a settings catalog policy targets a subset of a group."""
        filters = self.client_beta.device_management.assignment_filters
        self.assertTrue(str(filters.resource_path).endswith("/assignmentFilters"))

        filters.top(5).get().execute_query()
