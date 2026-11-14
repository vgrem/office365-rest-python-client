"""Device records: what Intune observed *about* a fleet, as against the fleet itself.

``managedDevices`` answers "which devices"; these families answer "what happened to them" - a
configuration conflict, a user-state tally, a restricted app someone ran, an encryption
finding, a certificate that is about to expire, a remote action. Each is a beta-only member of
``deviceManagement`` and each is read-only: there is nothing here to create, only to report.

The scopes are the two the reference pages publish - the configuration families answer to
``DeviceManagementConfiguration``, the device families to ``DeviceManagementManagedDevices``.
Domain join connectors have no REST page; the beta cmdlet that publishes the same type is
guarded by ``DeviceManagementServiceConfig``, and that is the scope asserted here.
"""

from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.intune.audit.remote_action_audit import RemoteActionAudit
from office365.intune.devices.compliance.restricted_apps_violation import RestrictedAppsViolation
from office365.intune.devices.configurations.conflict_summary import DeviceConfigurationConflictSummary
from office365.intune.devices.configurations.user_state_summary import DeviceConfigurationUserStateSummary
from office365.intune.devices.management.comanagement_eligible_device import ComanagementEligibleDevice
from office365.intune.devices.management.managed.all_device_certificate_state import (
    ManagedAllDeviceCertificateState,
)
from office365.intune.devices.management.managed.encryption_state import ManagedDeviceEncryptionState

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

CONFIGURATION = (
    "DeviceManagementConfiguration.Read.All",
    "DeviceManagementConfiguration.ReadWrite.All",
)

MANAGED_DEVICES = (
    "DeviceManagementManagedDevices.Read.All",
    "DeviceManagementManagedDevices.ReadWrite.All",
)

SERVICE_CONFIG = (
    "DeviceManagementServiceConfig.Read.All",
    "DeviceManagementServiceConfig.ReadWrite.All",
)


class TestDeviceRecords(GraphDelegatedTestCase):
    """The read-only families that record an observation about a device."""

    @requires_delegated(*CONFIGURATION)
    def test_01_configuration_records_are_listed(self):
        """A conflict, an app violation, an encryption finding and a certificate read alike.

        Four families, one shape: a collection under ``deviceManagement`` that reports what the
        service saw. An unprovisioned tenant answers with an empty collection, which is a
        successful read and the case a first-time tenant actually meets.
        """
        device_management = self.client_beta.device_management
        families = {
            "deviceConfigurationConflictSummary": (
                device_management.device_configuration_conflict_summary,
                DeviceConfigurationConflictSummary,
            ),
            "deviceConfigurationRestrictedAppsViolations": (
                device_management.device_configuration_restricted_apps_violations,
                RestrictedAppsViolation,
            ),
            "managedDeviceEncryptionStates": (
                device_management.managed_device_encryption_states,
                ManagedDeviceEncryptionState,
            ),
            "deviceConfigurationsAllManagedDeviceCertificateStates": (
                device_management.device_configurations_all_managed_device_certificate_states,
                ManagedAllDeviceCertificateState,
            ),
        }
        for name, (family, model) in families.items():
            with self.subTest(family=name):
                self.assertTrue(str(family.resource_path).endswith(f"/deviceManagement/{name}"))

                rows = family.top(5).get().execute_query()

                self.assertIsInstance(rows, EntityCollection)
                if len(rows):
                    self.assertIsInstance(rows[0], model)

    @requires_delegated(*CONFIGURATION)
    def test_02_the_user_state_tally_is_one_object(self):
        """``deviceConfigurationUserStateSummaries`` is a singleton: the fleet has one tally."""
        summary = self.client_beta.device_management.device_configuration_user_state_summaries.get().execute_query()

        self.assertIsInstance(summary, DeviceConfigurationUserStateSummary)
        self.assertIsNotNone(summary.id)

    @requires_delegated(*MANAGED_DEVICES)
    def test_03_device_families_report_actions_and_comanagement(self):
        """A remote action audit and a comanagement candidate are device facts, not configuration."""
        device_management = self.client_beta.device_management
        families = {
            "remoteActionAudits": (device_management.remote_action_audits, RemoteActionAudit),
            "comanagementEligibleDevices": (
                device_management.comanagement_eligible_devices,
                ComanagementEligibleDevice,
            ),
        }
        for name, (family, model) in families.items():
            with self.subTest(family=name):
                self.assertTrue(str(family.resource_path).endswith(f"/deviceManagement/{name}"))

                rows = family.top(5).get().execute_query()

                self.assertIsInstance(rows, EntityCollection)
                if len(rows):
                    self.assertIsInstance(rows[0], model)

    @requires_delegated(*SERVICE_CONFIG)
    def test_04_domain_join_connectors_are_listed(self):
        """A connector is the on-premises account that hybrid-joins a device."""
        connectors = self.client_beta.device_management.domain_join_connectors
        self.assertTrue(str(connectors.resource_path).endswith("/deviceManagement/domainJoinConnectors"))

        connectors.top(5).get().execute_query()
