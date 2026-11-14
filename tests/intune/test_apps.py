"""``deviceAppManagement``: the second Intune service root, and the app catalogue behind it.

Intune is not one root but two. ``deviceAppManagement`` exists on ``v1.0`` and carries the app
catalogue, the app protection policies and the MAM status; ``policySets`` and the assignment
machinery around the catalogue exist on ``beta`` only.
"""

from __future__ import annotations

from office365.intune.devices.management.app_management import DeviceAppManagement

from tests.decorators import requires_delegated
from tests.intune.intune_case import APPS, IntuneCase


class TestAppCatalogue(IntuneCase):
    """What the tenant distributes, and what it protects."""

    @requires_delegated(*APPS)
    def test_01_the_root_object_answers_for_the_tenant(self):
        """``GET deviceAppManagement`` is a second service root, not a child of the first."""
        root = self.client.device_app_management.get().execute_query()

        self.assertIsInstance(root, DeviceAppManagement)
        self.assertTrue(str(root.resource_path).endswith("/deviceAppManagement"))

    @requires_delegated(*APPS)
    def test_02_mobile_apps_are_listed(self):
        """The catalogue is one collection whatever the app kind."""
        self.read(self.client.device_app_management.mobile_apps, "mobileApps")

    @requires_delegated(*APPS)
    def test_03_app_categories_are_listed(self):
        """A category is a tenant-defined label, like a device category, but for apps."""
        self.read(self.client.device_app_management.mobile_app_categories, "mobileAppCategories")

    @requires_delegated(*APPS)
    def test_04_app_protection_policies_are_listed(self):
        """A managed-app policy is MAM: it protects data inside an app, not the device."""
        self.read(self.client.device_app_management.managed_app_policies, "managedAppPolicies")

    @requires_delegated(*APPS)
    def test_05_app_statuses_are_listed(self):
        """``managedAppStatuses`` is the deployment state of a managed app."""
        self.read(self.client.device_app_management.managed_app_statuses, "managedAppStatuses")

    @requires_delegated(*APPS)
    def test_06_policy_sets_are_a_preview_only_collection(self):
        """A policy set groups policies across Intune into one assignment, and beta only has it."""
        self.read(self.client_beta.device_app_management.policy_sets, "policySets")
