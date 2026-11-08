"""Device categories — a policy object created, read, renamed, and removed.

A device category is one of the few Intune objects a third-party app may create:
it carries nothing but a name, and Graph grants it under
``DeviceManagementManagedDevices.ReadWrite.All``. Policy objects proper —
configuration profiles, compliance policies, Terms and Conditions, Autopilot
identities — need ``DeviceManagementConfiguration.ReadWrite.All`` or
``DeviceManagementServiceConfig.ReadWrite.All``, which this app does not hold;
those are covered in ``test_device_management.py`` by reading what the tenant has.

The test removes what it created even when an assertion fails, so a bad run
leaves the tenant as it found it. Its name carries a per-run suffix: a shared
tenant must not make ``find_by_display_name`` ambiguous.
"""

from __future__ import annotations

from uuid import uuid4

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
        name = f"SDK Test Category {uuid4().hex[:8]}"
        renamed = f"{name} (renamed)"
        category = categories.add(displayName=name)
        try:
            category.execute_query()
            self.assertIsNotNone(category.id)
            self.assertEqual(category.display_name, name)
            self.assertTrue(str(category.resource_path).endswith(f"/deviceCategories/{category.id}"))

            category.set_property("displayName", renamed)
            category.update().execute_query()

            found = categories.find_by_display_name(renamed, required=True).execute_query()
            self.assertEqual(found.id, category.id, "the service must list the category under its new name")
        finally:
            if category.resource_path:
                category.delete_object().execute_query()

        self.assertFalse(categories.find_by_display_name(renamed).execute_query().is_loaded)
