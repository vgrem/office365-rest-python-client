"""Enrollment: how a device gets into Intune, and who is allowed to wipe it.

These are the *service configuration* families, the ones Intune guards with
``DeviceManagementServiceConfig``. The app under test holds only the configuration and managed
device scopes, so most of these reads skip here with the set named - which is the useful
outcome, because a tenant that grants them runs the same code unchanged.
"""

from __future__ import annotations

from office365.intune.devices.enrollment.android_device_owner_enrollment_profile import (
    AndroidDeviceOwnerEnrollmentProfile,
)
from office365.intune.devices.enrollment.android_for_work_settings import AndroidForWorkSettings
from office365.intune.devices.management.autopilot_event import DeviceManagementAutopilotEvent
from office365.runtime.types.odata_property import NotSupportedInVersion

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


class TestEnrollmentProfiles(IntuneCase):
    """Where a device registers itself, split by which half of the service guards it.

    Measured on this tenant: the Android programme and the Autopilot event log answer ``200``
    with the configuration scope alone, while the Apple/DEP side refuses with a message that
    names ``DeviceManagementServiceConfiguration`` - the two are guarded differently, and a
    suite that used one scope for both would have to skip work it can actually do.
    """

    @requires_delegated(*CONFIGURATION)
    def test_01_android_enrolment_profiles_are_two_kinds_of_token(self):
        """Device-owner and work-profile enrolment each mint their own token collection."""
        for profiles, segment in (
            (self.dm_beta.android_device_owner_enrollment_profiles, "androidDeviceOwnerEnrollmentProfiles"),
            (self.dm_beta.android_for_work_enrollment_profiles, "androidForWorkEnrollmentProfiles"),
        ):
            rows = self.read(profiles, segment)

            self.assertIsInstance(rows._item_type, type)
            self.assertTrue(str(rows.resource_path).endswith(f"/deviceManagement/{segment}"))

    @requires_delegated(*CONFIGURATION)
    def test_02_android_enterprise_settings_are_the_one_singleton(self):
        """`androidForWorkSettings` is a tenant-wide switch, so it is read without a collection."""
        settings = self.dm_beta.android_for_work_settings

        self.assertIsInstance(settings, AndroidForWorkSettings)
        self.assertTrue(str(settings.resource_path).endswith("/deviceManagement/androidForWorkSettings"))
        self.assertIsInstance(settings.get().execute_query(), AndroidForWorkSettings)

    @requires_delegated(*CONFIGURATION)
    def test_03_the_autopilot_event_log_is_a_record_of_attempts(self):
        """An Autopilot event is a per-device step, kept after the fact, not a queue."""
        rows = self.read(self.dm_beta.autopilot_events, "autopilotEvents")

        self.assertIs(rows._item_type, DeviceManagementAutopilotEvent)

    @requires_delegated(*SERVICE_CONFIG)
    def test_04_the_apple_programme_is_service_configuration(self):
        """A DEP token and an Apple profile are programme credentials, not device settings."""
        self.read(self.dm_beta.dep_onboarding_settings, "depOnboardingSettings")
        self.read(self.dm_beta.apple_user_initiated_enrollment_profiles, "appleUserInitiatedEnrollmentProfiles")

    @requires_delegated(*SERVICE_CONFIG)
    def test_05_imported_identities_and_autopilot_settings_agree_with_dep(self):
        """Same guard, same reason: both are filled in by an administrator, not a device."""
        self.read(self.dm_beta.imported_device_identities, "importedDeviceIdentities")
        self.read(self.dm_beta.windows_autopilot_settings, "windowsAutopilotSettings")

    def test_06_the_stable_root_refuses_every_one_of_them(self):
        """Batch 9's eight navigations are absent from `Graph.xml`, so v1.0 answers first."""
        for name in (
            "android_device_owner_enrollment_profiles",
            "android_for_work_enrollment_profiles",
            "android_for_work_settings",
            "apple_user_initiated_enrollment_profiles",
            "dep_onboarding_settings",
            "imported_device_identities",
            "windows_autopilot_settings",
            "autopilot_events",
        ):
            with self.subTest(member=name):
                with self.assertRaises(NotSupportedInVersion):
                    getattr(self.dm, name)

        with self.assertRaises(NotSupportedInVersion):
            AndroidDeviceOwnerEnrollmentProfile(self.client)
