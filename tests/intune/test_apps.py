"""``deviceAppManagement``: the second Intune service root, and the app catalogue behind it.

Intune is not one root but two. ``deviceAppManagement`` exists on ``v1.0`` and carries the app
catalogue, the app protection policies and the MAM status; ``policySets`` and the assignment
machinery around the catalogue exist on ``beta`` only.

The beta-only half of that root is the record side: the devices MAM registered, the wipes it
queued, the Windows protection policies it applies, the WDAC supplemental policies and the iOS
LOB provisioning profiles it distributes, and the partner-integration tasks it leaves for an
administrator. Every one of them publishes ``DeviceManagementApps`` - reads included, which is
why the family needs a grant before it needs a test. ``mobileAppCatalogPackages`` is the one
exception: it has no reference page and no cmdlet, so no scope can be declared for it here and
its test asserts the shape of the path only.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.devices.management.app_management import DeviceAppManagement
from office365.intune.devices.management.app_management_task import DeviceAppManagementTask
from office365.intune.devices.management.managed.app.protections.windows_managed_app_protection import (
    WindowsManagedAppProtection,
)
from office365.intune.devices.management.mobileapps.ios.lob_app_provisioning_configuration import (
    IosLobAppProvisioningConfiguration,
)
from office365.intune.devices.management.mobileapps.mobile_app_catalog_package import MobileAppCatalogPackage
from office365.intune.devices.management.windows_defender_application_control_supplemental_policy import (
    WindowsDefenderApplicationControlSupplementalPolicy,
)
from office365.intune.devices.management.windows_information_protection_device_registration import (
    WindowsInformationProtectionDeviceRegistration,
)
from office365.intune.devices.management.windows_information_protection_wipe_action import (
    WindowsInformationProtectionWipeAction,
)
from office365.intune.devices.management.windows_management_app import WindowsManagementApp

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

#: Every beta-only family of ``deviceAppManagement`` answers to the apps scope, reads included.
APPS = (
    "DeviceManagementApps.Read.All",
    "DeviceManagementApps.ReadWrite.All",
)


class TestAppCatalogue(GraphDelegatedTestCase):
    """What the tenant distributes, and what it protects."""

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_01_the_root_object_answers_for_the_tenant(self):
        """``GET deviceAppManagement`` is a second service root, not a child of the first."""
        root = self.client.device_app_management.get().execute_query()

        self.assertIsInstance(root, DeviceAppManagement)
        self.assertTrue(str(root.resource_path).endswith("/deviceAppManagement"))

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_02_mobile_apps_are_listed(self):
        """The catalogue is one collection whatever the app kind."""
        apps = self.client.device_app_management.mobile_apps
        self.assertTrue(str(apps.resource_path).endswith("/mobileApps"))

        apps.top(5).get().execute_query()

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_03_app_categories_are_listed(self):
        """A category is a tenant-defined label, like a device category, but for apps."""
        categories = self.client.device_app_management.mobile_app_categories
        self.assertTrue(str(categories.resource_path).endswith("/mobileAppCategories"))

        categories.top(5).get().execute_query()

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_04_app_protection_policies_are_listed(self):
        """A managed-app policy is MAM: it protects data inside an app, not the device."""
        policies = self.client.device_app_management.managed_app_policies
        self.assertTrue(str(policies.resource_path).endswith("/managedAppPolicies"))

        policies.top(5).get().execute_query()

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_05_app_statuses_are_listed(self):
        """``managedAppStatuses`` is the deployment state of a managed app."""
        statuses = self.client.device_app_management.managed_app_statuses
        self.assertTrue(str(statuses.resource_path).endswith("/managedAppStatuses"))

        statuses.top(5).get().execute_query()

    @requires_delegated("DeviceManagementApps.Read.All", "DeviceManagementApps.ReadWrite.All")
    def test_06_policy_sets_are_a_preview_only_collection(self):
        """A policy set groups policies across Intune into one assignment, and beta only has it."""
        policy_sets = self.client_beta.device_app_management.policy_sets
        self.assertTrue(str(policy_sets.resource_path).endswith("/policySets"))

        policy_sets.top(5).get().execute_query()


class TestAppManagementRecords(GraphDelegatedTestCase):
    """The record families ``beta`` keeps behind ``deviceAppManagement``."""

    @requires_delegated(*APPS)
    def test_07_the_mam_records_are_listed(self):
        """A registered device, a queued wipe and a Windows protection policy are MAM records.

        They share one scope and one shape - a collection under ``deviceAppManagement`` that a
        tenant which has never enrolled a device answers with an empty page, which is still a
        successful read.
        """
        root = self.client_beta.device_app_management
        families = {
            "windowsInformationProtectionDeviceRegistrations": (
                root.windows_information_protection_device_registrations,
                WindowsInformationProtectionDeviceRegistration,
            ),
            "windowsInformationProtectionWipeActions": (
                root.windows_information_protection_wipe_actions,
                WindowsInformationProtectionWipeAction,
            ),
            "windowsManagedAppProtections": (root.windows_managed_app_protections, WindowsManagedAppProtection),
        }
        for name, (family, model) in families.items():
            with self.subTest(family=name):
                self.assertTrue(str(family.resource_path).endswith(f"/deviceAppManagement/{name}"))

                rows = family.top(5).get().execute_query()

                self.assertIsInstance(rows, EntityCollection)
                if len(rows):
                    self.assertIsInstance(rows[0], model)

    @requires_delegated(*APPS)
    def test_08_what_the_tenant_hands_out_and_what_it_asks_for(self):
        """A WDAC supplemental policy, an iOS provisioning profile and a partner task.

        The first two are content uploaded so an app can run; the third is a finding an
        administrator has to close, which is why it carries a status rather than a payload.
        """
        root = self.client_beta.device_app_management
        families = {
            "wdacSupplementalPolicies": (
                root.wdac_supplemental_policies,
                WindowsDefenderApplicationControlSupplementalPolicy,
            ),
            "iosLobAppProvisioningConfigurations": (
                root.ios_lob_app_provisioning_configurations,
                IosLobAppProvisioningConfiguration,
            ),
            "deviceAppManagementTasks": (root.device_app_management_tasks, DeviceAppManagementTask),
        }
        for name, (family, model) in families.items():
            with self.subTest(family=name):
                self.assertTrue(str(family.resource_path).endswith(f"/deviceAppManagement/{name}"))

                rows = family.top(5).get().execute_query()

                self.assertIsInstance(rows, EntityCollection)
                if len(rows):
                    self.assertIsInstance(rows[0], model)

    @requires_delegated(*APPS)
    def test_09_the_management_agent_reports_its_health(self):
        """``windowsManagementApp`` is one object: the tenant has an agent or it has not."""
        agent = self.client_beta.device_app_management.windows_management_app.get().execute_query()

        self.assertIsInstance(agent, WindowsManagementApp)
        self.assertTrue(str(agent.resource_path).endswith("/deviceAppManagement/windowsManagementApp"))

        self.assertTrue(str(agent.health_states.resource_path).endswith("/windowsManagementApp/healthStates"))
        agent.health_states.top(5).get().execute_query()

    def test_10_a_family_without_a_reference_page_is_addressed_by_shape(self):
        """``mobileAppCatalogPackages`` publishes no permission table, so no scope is asserted.

        The path is still checkable, and that is the whole assertion: the getter exists, it
        builds one collection, and nothing here claims what it would cost to read.
        """
        packages = self.client_beta.device_app_management.mobile_app_catalog_packages

        self.assertIsInstance(packages, EntityCollection)
        self.assertIs(packages._item_type, MobileAppCatalogPackage)
        self.assertTrue(str(packages.resource_path).endswith("/deviceAppManagement/mobileAppCatalogPackages"))
