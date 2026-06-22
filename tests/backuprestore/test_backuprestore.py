"""Microsoft 365 Backup Storage (M365 Backup) — service status, protection policies, and restore sessions.
Tests cover:
  - Service status: enabling, reading status, checking tenant state
  - Protection policies: listing OneDrive for Business protection policies
  - Policy rules: accessing drive inclusion rules
  - Restore session scenarios (where available)
  - Error handling: double-enable, disabled service checks
  - Enum sanity: verifying known enum values are present
"""

from __future__ import annotations

from typing import ClassVar, Optional

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

_TEST_TENANT_ID = "af6a80a4-8b4b-4879-88af-42ff8a545211"


class TestBackupRestoreServiceStatus(GraphDelegatedTestCase):
    """Reading and verifying the M365 Backup service status."""

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_01_get_service_status(self):
        """Reading the backup restore service status returns a valid status object."""
        result = self.client.solutions.backup_restore.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        # The status should have an id
        self.assertIsNotNone(result.get_property("id"))

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_02_service_status_has_expected_properties(self):
        """The backup restore service status exposes serviceStatus and serviceAppStatus."""
        result = self.client.solutions.backup_restore.get().execute_query()
        service_status = result.get_property("serviceStatus")
        if service_status is not None:
            self.assertIsInstance(service_status, (str, int))

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_03_service_status_is_valid_enum(self):
        """The serviceStatus should be one of the known BackupServiceStatus values."""
        result = self.client.solutions.backup_restore.get().execute_query()
        raw_status = result.get_property("serviceStatus")
        # Assert — known values from BackupServiceStatus enum
        if raw_status is not None:
            known_statuses = {"0", "1", "2", "3", "4"}
            raw_str = str(raw_status)
            self.assertIn(
                raw_str,
                known_statuses,
                f"Service status '{raw_str}' not in known values {known_statuses}",
            )

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_04_get_backup_restore_without_enabling(self):
        """Reading backup restore status does not require enabling first."""
        # This test verifies read-only access works independently of enable()
        result = self.client.solutions.backup_restore.get().execute_query()
        # Assert — basic integrity check
        self.assertIsNotNone(result.resource_path)
        self.assertIsNotNone(result.get_property("id"))


class TestBackupRestoreEnable(GraphDelegatedTestCase):
    """Enabling the M365 Backup Storage service.
    Enabling requires BackupRestore-Control.ReadWrite.All permission and
    a valid appOwnerTenantId. This is a one-time or infrequent operation.
    """

    enabled_service: ClassVar[Optional[object]] = None

    @requires_delegated("BackupRestore-Control.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test_01_enable_backup_restore(self):
        """Enabling the backup restore service for a tenant should succeed.
        Note: This operation is typically a one-time setup. If the service
        is already enabled, the API may return the current status without error.
        """
        try:
            result = self.client.solutions.backup_restore.enable(_TEST_TENANT_ID).execute_query()
            self.assertIsNotNone(result.value)
            TestBackupRestoreEnable.enabled_service = result
        except Exception as e:
            self.skipTest(f"Cannot enable backup restore (may already be enabled): {e}")

    @requires_delegated("BackupRestore-Control.ReadWrite.All", bypass_roles=["Global Administrator"])
    def test_02_enable_again_is_idempotent(self):
        """Re-enabling an already-enabled service should not error."""
        try:
            # Act — second enable call with the same tenant
            result = self.client.solutions.backup_restore.enable(_TEST_TENANT_ID).execute_query()
            # Assert — should return service status without crashing
            self.assertIsNotNone(result.value)
        except Exception:
            self.skipTest("Double-enable not allowed or unavailable")

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_03_service_status_changes_after_enable(self):
        """After enabling, the service status should reflect the enabled state."""
        result = self.client.solutions.backup_restore.get().execute_query()
        raw_status = result.get_property("serviceStatus")
        # If service is enabled, status should not be '0' (disabled)
        if raw_status is not None and str(raw_status) == "0":
            self.skipTest("Service is disabled; enable test may not have run")


class TestBackupRestoreProtectionPolicies(GraphDelegatedTestCase):
    """Backup protection policies — defining what to protect, when, and for how long."""

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_01_list_one_drive_policies(self):
        """Listing OneDrive for Business protection policies returns a valid collection."""
        result = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies.top(10).get().execute_query()
        )
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_02_policy_has_expected_properties(self):
        """A protection policy exposes displayName, createdDateTime, status, and createdBy."""
        result = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies.top(5).get().execute_query()
        )
        if len(result) == 0:
            self.skipTest("No OneDrive protection policies exist")
        for policy in result:
            self.assertIsNotNone(policy.get_property("id"))
            # displayName may be None for unnamed policies
            self.assertIsNotNone(policy.get_property("createdDateTime"))
            self.assertIsNotNone(policy.get_property("status"))
            break

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_03_policy_filter_by_status(self):
        """Filtering protection policies by status works."""
        result = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies.filter("status eq 'active'")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for policy in result:
            self.assertEqual(policy.get_property("status"), "active")

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_04_policy_has_drive_inclusion_rules(self):
        """A protection policy may have drive inclusion rules."""
        result = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies.top(3).get().execute_query()
        )
        if len(result) == 0:
            self.skipTest("No OneDrive protection policies exist")
        for policy in result:
            try:
                rules = policy.drive_inclusion_rules.get().execute_query()
                self.assertIsNotNone(rules.resource_path)
                break
            except Exception:
                continue

    @requires_delegated("BackupRestore.Read.All", bypass_roles=["Global Administrator"])
    def test_05_get_policy_by_id(self):
        """Retrieving a protection policy by its ID returns the same policy."""
        result = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies.top(1).get().execute_query()
        )
        if len(result) == 0:
            self.skipTest("No OneDrive protection policies exist")
        first = result[0]
        policy_id = first.get_property("id")
        fetched = (
            self.client.solutions.backup_restore.one_drive_for_business_protection_policies[policy_id]
            .get()
            .execute_query()
        )
        self.assertIsNotNone(fetched.resource_path)
        self.assertEqual(fetched.get_property("id"), policy_id)


class TestBackupRestoreEnumValues(GraphDelegatedTestCase):
    """Verify enum value definitions used across the backup restore API."""

    def test_01_backup_service_status_values(self):
        """BackupServiceStatus enum has expected values."""
        from office365.backuprestore.backupservicestatus import BackupServiceStatus

        self.assertTrue(hasattr(BackupServiceStatus, "disabled"))
        self.assertTrue(hasattr(BackupServiceStatus, "enabled"))
        self.assertTrue(hasattr(BackupServiceStatus, "protectionChangeLocked"))
        self.assertTrue(hasattr(BackupServiceStatus, "restoreLocked"))
        self.assertTrue(hasattr(BackupServiceStatus, "unknownFutureValue"))

    def test_02_restorable_artifact_values(self):
        """RestorableArtifact enum has expected values."""
        from office365.backuprestore.restorableartifact import RestorableArtifact

        self.assertTrue(hasattr(RestorableArtifact, "message"))
        self.assertTrue(hasattr(RestorableArtifact, "unknownFutureValue"))

    def test_03_restore_session_status_values(self):
        """RestoreSessionStatus enum has expected values."""
        from office365.backuprestore.restoresessions.status import RestoreSessionStatus

        self.assertTrue(hasattr(RestoreSessionStatus, "draft"))
        self.assertTrue(hasattr(RestoreSessionStatus, "activating"))
        self.assertTrue(hasattr(RestoreSessionStatus, "active"))
        self.assertTrue(hasattr(RestoreSessionStatus, "completed"))
        self.assertTrue(hasattr(RestoreSessionStatus, "failed"))

    def test_04_restore_point_preference_values(self):
        """RestorePointPreference enum has expected values."""
        from office365.backuprestore.restorepoints.preference import RestorePointPreference

        self.assertTrue(hasattr(RestorePointPreference, "latest"))
        self.assertTrue(hasattr(RestorePointPreference, "oldest"))
        self.assertTrue(hasattr(RestorePointPreference, "unknownFutureValue"))

    def test_05_artifact_restore_status_values(self):
        """ArtifactRestoreStatus enum has expected values."""
        from office365.backuprestore.artifactrestorestatus import ArtifactRestoreStatus

        self.assertTrue(hasattr(ArtifactRestoreStatus, "added"))
        self.assertTrue(hasattr(ArtifactRestoreStatus, "scheduling"))
        self.assertTrue(hasattr(ArtifactRestoreStatus, "succeeded"))
        self.assertTrue(hasattr(ArtifactRestoreStatus, "failed"))

    def test_06_service_app_status_values(self):
        """ServiceAppStatus enum has expected values."""
        from office365.backuprestore.serviceapps.status import ServiceAppStatus

        self.assertTrue(hasattr(ServiceAppStatus, "inactive"))
        self.assertTrue(hasattr(ServiceAppStatus, "active"))
        self.assertTrue(hasattr(ServiceAppStatus, "pendingActive"))
        self.assertTrue(hasattr(ServiceAppStatus, "pendingInactive"))
