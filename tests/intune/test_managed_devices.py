"""``managedDevices``: the enrolled-device inventory, and what hangs off one enrolled device.

Intune is not activated on the test tenant, so the inventory is empty here and every test that
needs a row skips naming it. What the reads still prove is the important half: the path each
member addresses, the type the collection declares, and that a query option is translated
rather than dropped.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.devices.management.managed.managed import ManagedDevice

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

#: A remote action is a privileged operation: Intune wants this scope for ``syncDevice`` and
#: the model declares it on the method. Provenance: measured.
PRIVILEGED_OPERATIONS = "DeviceManagementManagedDevices.PrivilegedOperations.All"

#: ``managedDevices``, ``detectedApps``, the overview and the per-device state lists.
MANAGED_DEVICES = (
    "DeviceManagementManagedDevices.Read.All",
    "DeviceManagementManagedDevices.ReadWrite.All",
)


class TestManagedDeviceInventory(GraphDelegatedTestCase):
    """Reading the inventory a tenant-wide report starts from."""

    @requires_delegated(*MANAGED_DEVICES)
    def test_01_the_inventory_declares_the_type_it_holds(self):
        """``managedDevices`` is the one Intune collection that states its item type."""
        devices = self.client.device_management.managed_devices
        self.assertTrue(str(devices.resource_path).endswith("/managedDevices"))

        rows = devices.top(5).get().execute_query()

        self.assertIsInstance(rows, EntityCollection)
        self.assertIs(rows.item_type(), ManagedDevice)

    @requires_delegated(*MANAGED_DEVICES)
    def test_02_a_projection_returns_the_columns_asked_for(self):
        """``$select`` reaches the wire: the rows carry what was asked and nothing else."""
        query = self.client.device_management.managed_devices.select(["id", "deviceName", "complianceState"])
        self.assertTrue(str(query.resource_path).endswith("/managedDevices"))

        rows = query.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no managed device")

        columns = set(rows[0].properties)
        self.assertTrue({"id", "deviceName", "complianceState"} <= columns, columns)
        self.assertNotIn("serialNumber", columns)

    @requires_delegated(*MANAGED_DEVICES)
    def test_03_the_caller_sees_the_devices_it_manages(self):
        """``me/managedDevices`` addresses the same rows, scoped to the signed-in user."""
        devices = self.client.me.managed_devices
        self.assertTrue(str(devices.resource_path).endswith("/managedDevices"))

        devices.top(5).get().execute_query()

    @requires_delegated(*MANAGED_DEVICES)
    def test_04_the_overview_is_a_singleton(self):
        """``managedDeviceOverview`` counts the estate and is one object, not a collection."""
        overview = self.client.device_management.managed_device_overview

        self.assertNotIsInstance(overview, EntityCollection)
        self.assertIsInstance(overview.get().execute_query(), type(overview))

    @requires_delegated(*MANAGED_DEVICES)
    def test_05_detected_apps_are_a_tenant_wide_collection(self):
        """``detectedApps`` is what Intune discovered on the managed devices."""
        apps = self.client.device_management.detected_apps
        self.assertTrue(str(apps.resource_path).endswith("/detectedApps"))

        apps.top(5).get().execute_query()


class TestOneManagedDevice(GraphDelegatedTestCase):
    """What a suite may read once a device exists - and what it does when none does."""

    @requires_delegated(*MANAGED_DEVICES)
    def test_01_a_device_reports_its_compliance_per_policy(self):
        """The per-policy compliance states of one device hang off that device."""
        rows = self.client.device_management.managed_devices.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no managed device")

        device = rows[0]
        states = device.device_compliance_policy_states.top(5).get().execute_query()

        self.assertIn(f"/managedDevices/{device.id}/deviceCompliancePolicyStates", str(states.resource_path))

    @requires_delegated(PRIVILEGED_OPERATIONS)
    def test_02_a_remote_action_is_accepted_for_an_enrolled_device(self):
        """``syncDevice`` forces a check-in: an action, not an update, and it needs its own scope."""
        rows = self.client.device_management.managed_devices.top(5).get().execute_query()
        if not len(rows):
            self.skipTest("this tenant holds no managed device")

        device = rows[0]
        device.sync_device().execute_query()

        self.assertIsNotNone(device.id)
