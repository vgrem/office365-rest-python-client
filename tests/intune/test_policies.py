"""Policies: what the tenant enforces, on the settings the service actually ships.

Two generations live side by side. ``deviceConfigurations`` and ``deviceCompliancePolicies`` are
the classic profiles and exist on ``v1.0``; ``configurationPolicies`` is the Settings Catalog and
exists on ``beta`` only, where ``compliancePolicies`` mirrors it for compliance. A suite that
means the settings catalog has to say so by naming ``dm_beta``.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, IntuneCase


class TestClassicPolicies(IntuneCase):
    """The profiles the stable root carries."""

    @requires_delegated(*CONFIGURATION)
    def test_01_device_configurations_are_listed(self):
        """A configuration profile is addressed by ``/deviceConfigurations``."""
        self.read(self.dm.device_configurations, "deviceConfigurations")

    @requires_delegated(*CONFIGURATION)
    def test_02_a_profile_names_its_platform(self):
        """One collection carries every platform, and ``@odata.type`` says which one a row is."""
        profile = self.row_or_skip(
            self.read(self.dm.device_configurations, "deviceConfigurations"), "configuration profile"
        )

        self.assertIsNotNone(profile.get_property("displayName"))
        self.assertIsNotNone(profile.get_property("@odata.type"))

    @requires_delegated(*CONFIGURATION)
    def test_03_compliance_policies_are_listed(self):
        """Compliance policies are a separate family from configuration profiles."""
        self.read(self.dm.device_compliance_policies, "deviceCompliancePolicies")

    @requires_delegated(*CONFIGURATION)
    def test_04_a_compliance_policy_carries_its_assignments(self):
        """An assignment is a navigation off the policy, so an unassigned policy answers empty."""
        policy = self.row_or_skip(
            self.read(self.dm.device_compliance_policies, "deviceCompliancePolicies"), "compliance policy"
        )
        assignments = policy.assignments.top(5).get().execute_query()

        self.assertIn(f"/deviceCompliancePolicies/{policy.id}/assignments", str(assignments.resource_path))


class TestSettingsCatalog(IntuneCase):
    """The preview-root families that replaced the classic profiles."""

    @requires_delegated(*CONFIGURATION)
    def test_01_configuration_policies_are_listed(self):
        """``configurationPolicies`` is the Settings Catalog, and v1.0 has no such segment."""
        self.read(self.dm_beta.configuration_policies, "configurationPolicies")

    @requires_delegated(*CONFIGURATION)
    def test_02_the_catalog_ships_templates(self):
        """A template is a policy skeleton the tenant gets for free, so it needs no enrolment."""
        templates = self.read(self.dm_beta.configuration_policy_templates, "configurationPolicyTemplates")
        template = self.row_or_skip(templates, "settings catalog template")

        self.assertIsNotNone(template.get_property("displayName"))

    @requires_delegated(*CONFIGURATION)
    def test_03_compliance_policies_are_listed_on_the_preview_root(self):
        """The catalog-era compliance family answers under ``compliancePolicies``."""
        self.read(self.dm_beta.compliance_policies, "compliancePolicies")

    @requires_delegated(*CONFIGURATION)
    def test_04_assignment_filters_are_listed(self):
        """A filter is how a settings catalog policy targets a subset of a group."""
        self.read(self.dm_beta.assignment_filters, "assignmentFilters")
