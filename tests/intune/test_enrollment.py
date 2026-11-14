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
from tests.graph_case import GraphDelegatedTestCase

CONFIGURATION = (
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementConfiguration.ReadWrite.All",
)

SERVICE_CONFIG = (
    "DeviceManagementServiceConfig.Read.All",
    "DeviceManagementServiceConfig.ReadWrite.All",
)


class TestEnrollmentConfiguration(GraphDelegatedTestCase):
    """The rules a device meets on its way in."""

    @requires_delegated(*SERVICE_CONFIG)
    def test_01_enrollment_configurations_are_listed(self):
        """Device platform restrictions, limit sets and enrollment status pages share one path."""
        configurations = self.client_beta.device_management.device_enrollment_configurations
        self.assertTrue(str(configurations.resource_path).endswith("/deviceEnrollmentConfigurations"))

        configurations.top(5).get().execute_query()

    @requires_delegated(*SERVICE_CONFIG)
    def test_02_autopilot_deployment_profiles_are_listed(self):
        """An Autopilot profile is the out-of-box experience a new device boots into."""
        profiles = self.client_beta.device_management.windows_autopilot_deployment_profiles
        self.assertTrue(str(profiles.resource_path).endswith("/windowsAutopilotDeploymentProfiles"))

        profiles.top(5).get().execute_query()

    @requires_delegated(*SERVICE_CONFIG)
    def test_03_imported_autopilot_identities_are_listed(self):
        """A hardware hash imported ahead of time is how a device is claimed before it boots."""
        identities = self.client_beta.device_management.imported_windows_autopilot_device_identities
        self.assertTrue(str(identities.resource_path).endswith("/importedWindowsAutopilotDeviceIdentities"))

        identities.top(5).get().execute_query()


class TestServiceConfiguration(GraphDelegatedTestCase):
    """Tenant-wide switches, read as singletons or collections."""

    @requires_delegated(*CONFIGURATION)
    def test_01_android_enterprise_settings_are_a_singleton(self):
        """The managed-Google-Play binding is one object per tenant, not a collection."""
        settings = self.client_beta.device_management.android_managed_store_account_enterprise_settings

        self.assertIsInstance(settings.get().execute_query(), type(settings))

    @requires_delegated(*SERVICE_CONFIG)
    def test_02_terms_and_conditions_are_listed(self):
        """Terms and Conditions are an assignment target, so they are a collection."""
        terms = self.client.device_management.terms_and_conditions
        self.assertTrue(str(terms.resource_path).endswith("/termsAndConditions"))

        terms.top(5).get().execute_query()

    @requires_delegated(*SERVICE_CONFIG)
    def test_03_management_partners_are_listed(self):
        """A management partner is the reseller record attached to the tenant."""
        partners = self.client.device_management.device_management_partners
        self.assertTrue(str(partners.resource_path).endswith("/deviceManagementPartners"))

        partners.top(5).get().execute_query()

    @requires_delegated(*SERVICE_CONFIG)
    def test_04_mobile_threat_defense_connectors_are_listed(self):
        """A connector binds a third-party MTD product; Intune itself needs no such licence."""
        connectors = self.client.device_management.mobile_threat_defense_connectors
        self.assertTrue(str(connectors.resource_path).endswith("/mobileThreatDefenseConnectors"))

        connectors.top(5).get().execute_query()


class TestEnrollmentProfiles(GraphDelegatedTestCase):
    """Where a device registers itself, split by which half of the service guards it.

    Measured on this tenant: the Android programme and the Autopilot event log answer ``200``
    with the configuration scope alone, while the Apple/DEP side refuses with a message that
    names ``DeviceManagementServiceConfiguration`` - the two are guarded differently, and a
    suite that used one scope for both would have to skip work it can actually do.
    """

    @requires_delegated(*CONFIGURATION)
    def test_01_android_enrolment_profiles_are_two_kinds_of_token(self):
        """Device-owner and work-profile enrolment each mint their own token collection."""
        dm = self.client_beta.device_management
        for profiles, segment in (
            (dm.android_device_owner_enrollment_profiles, "androidDeviceOwnerEnrollmentProfiles"),
            (dm.android_for_work_enrollment_profiles, "androidForWorkEnrollmentProfiles"),
        ):
            self.assertTrue(str(profiles.resource_path).endswith(f"/deviceManagement/{segment}"))

            rows = profiles.top(5).get().execute_query()

            self.assertIsInstance(rows._item_type, type)

    @requires_delegated(*CONFIGURATION)
    def test_02_android_enterprise_settings_are_the_one_singleton(self):
        """`androidForWorkSettings` is a tenant-wide switch, so it is read without a collection."""
        settings = self.client_beta.device_management.android_for_work_settings

        self.assertIsInstance(settings, AndroidForWorkSettings)
        self.assertTrue(str(settings.resource_path).endswith("/deviceManagement/androidForWorkSettings"))
        self.assertIsInstance(settings.get().execute_query(), AndroidForWorkSettings)

    @requires_delegated(*CONFIGURATION)
    def test_03_the_autopilot_event_log_is_a_record_of_attempts(self):
        """An Autopilot event is a per-device step, kept after the fact, not a queue."""
        events = self.client_beta.device_management.autopilot_events
        self.assertTrue(str(events.resource_path).endswith("/autopilotEvents"))

        rows = events.top(5).get().execute_query()

        self.assertIs(rows._item_type, DeviceManagementAutopilotEvent)

    @requires_delegated(*SERVICE_CONFIG)
    def test_04_the_apple_programme_is_service_configuration(self):
        """A DEP token and an Apple profile are programme credentials, not device settings."""
        dm = self.client_beta.device_management
        self.assertTrue(str(dm.dep_onboarding_settings.resource_path).endswith("/depOnboardingSettings"))
        self.assertTrue(
            str(dm.apple_user_initiated_enrollment_profiles.resource_path).endswith(
                "/appleUserInitiatedEnrollmentProfiles"
            )
        )

        dm.dep_onboarding_settings.top(5).get().execute_query()
        dm.apple_user_initiated_enrollment_profiles.top(5).get().execute_query()

    @requires_delegated(*SERVICE_CONFIG)
    def test_05_imported_identities_and_autopilot_settings_agree_with_dep(self):
        """Same guard, same reason: both are filled in by an administrator, not a device."""
        dm = self.client_beta.device_management
        self.assertTrue(str(dm.imported_device_identities.resource_path).endswith("/importedDeviceIdentities"))
        self.assertTrue(str(dm.windows_autopilot_settings.resource_path).endswith("/windowsAutopilotSettings"))

        dm.imported_device_identities.top(5).get().execute_query()
        dm.windows_autopilot_settings.get().execute_query()

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
                    getattr(self.client.device_management, name)

        with self.assertRaises(NotSupportedInVersion):
            AndroidDeviceOwnerEnrollmentProfile(self.client)
