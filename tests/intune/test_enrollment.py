"""Enrollment: how a device gets into Intune, and who is allowed to wipe it.

These are the *service configuration* families, the ones Intune guards with
``DeviceManagementServiceConfig``. The app under test holds only the configuration and managed
device scopes, so most of these reads skip here with the set named - which is the useful
outcome, because a tenant that grants them runs the same code unchanged.
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.intune.intune_case import CONFIGURATION, SERVICE_CONFIG, IntuneCase


class TestEnrollmentConfiguration(IntuneCase):
    """The rules a device meets on its way in."""

    @requires_delegated(*SERVICE_CONFIG)
    def test_01_enrollment_configurations_are_listed(self):
        """Device platform restrictions, limit sets and enrollment status pages share one path."""
        self.read(self.dm_beta.device_enrollment_configurations, "deviceEnrollmentConfigurations")

    @requires_delegated(*SERVICE_CONFIG)
    def test_02_autopilot_deployment_profiles_are_listed(self):
        """An Autopilot profile is the out-of-box experience a new device boots into."""
        self.read(self.dm_beta.windows_autopilot_deployment_profiles, "windowsAutopilotDeploymentProfiles")

    @requires_delegated(*SERVICE_CONFIG)
    def test_03_imported_autopilot_identities_are_listed(self):
        """A hardware hash imported ahead of time is how a device is claimed before it boots."""
        self.read(
            self.dm_beta.imported_windows_autopilot_device_identities,
            "importedWindowsAutopilotDeviceIdentities",
        )


class TestServiceConfiguration(IntuneCase):
    """Tenant-wide switches, read as singletons or collections."""

    @requires_delegated(*CONFIGURATION)
    def test_01_android_enterprise_settings_are_a_singleton(self):
        """The managed-Google-Play binding is one object per tenant, not a collection."""
        settings = self.dm_beta.android_managed_store_account_enterprise_settings

        self.assertIsInstance(settings.get().execute_query(), type(settings))

    @requires_delegated(*SERVICE_CONFIG)
    def test_02_terms_and_conditions_are_listed(self):
        """Terms and Conditions are an assignment target, so they are a collection."""
        self.read(self.dm.terms_and_conditions, "termsAndConditions")

    @requires_delegated(*SERVICE_CONFIG)
    def test_03_management_partners_are_listed(self):
        """A management partner is the reseller record attached to the tenant."""
        self.read(self.dm.device_management_partners, "deviceManagementPartners")

    @requires_delegated(*SERVICE_CONFIG)
    def test_04_mobile_threat_defense_connectors_are_listed(self):
        """A connector binds a third-party MTD product; Intune itself needs no such licence."""
        self.read(self.dm.mobile_threat_defense_connectors, "mobileThreatDefenseConnectors")
