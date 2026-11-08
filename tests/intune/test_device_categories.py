"""Device categories — a policy object created, read, renamed, and removed.

A device category is one of the few Intune objects a third-party app may create:
it carries nothing but a name, and Graph grants it under
``DeviceManagementManagedDevices.ReadWrite.All``. Policy objects proper —
configuration profiles, compliance policies, Terms and Conditions, Autopilot
identities — need ``DeviceManagementConfiguration.ReadWrite.All`` or
``DeviceManagementServiceConfig.ReadWrite.All``, which this app does not hold;
those are covered in ``test_device_management.py`` by reading what the tenant has.

The test removes what it created even when an assertion fails, so a bad run
leaves the tenant as it found it.
"""

from __future__ import annotations

from office365.intune.devices.category import DeviceCategory
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDeviceCategories(GraphDelegatedTestCase):
    """One object through its whole life."""

    @requires_delegated(
        "DeviceManagementManagedDevices.ReadWrite.All",
        bypass_roles=["Intune Administrator", "Global Administrator"],
    )
    def test_01_a_category_can_be_created_renamed_and_removed(self):
        """Create, read back, rename, and delete a device category."""
        categories = self.client.device_management.device_categories
        category = categories.add(displayName="SDK Test Category")
        try:
            category.execute_query()
            self.assertIsNotNone(category.id)
            self.assertEqual(category.display_name, "SDK Test Category")
            self.assertTrue(str(category.resource_path).endswith(f"/deviceCategories/{category.id}"))

            category.set_property("displayName", "SDK Test Category (renamed)")
            category.update().execute_query()
            self.assertEqual(category.display_name, "SDK Test Category (renamed)")

            reloaded = self._find(category.id)
            self.assertIsNotNone(reloaded, "a category the service accepted must come back in the list")
            self.assertEqual(reloaded.get_property("displayName"), "SDK Test Category (renamed)")
        finally:
            if category.resource_path:
                category.delete_object().execute_query()

        self.assertIsNone(self._find(category.id))

    def _find(self, category_id: str) -> DeviceCategory | None:
        """The category with this id, as the service lists it — not the object we hold."""
        for category in self.client.device_management.device_categories.get().execute_query():
            if category.id == category_id:
                return category
        return None
