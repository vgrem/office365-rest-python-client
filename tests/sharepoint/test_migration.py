from __future__ import annotations

from typing import ClassVar, Optional

from office365.sharepoint.sites.azure_container_Info import (
    ProvisionedTemporaryAzureContainerInfo,
)

from tests.sharepoint.sharepoint_case import SPTestCase


class TestMigration(SPTestCase):
    """SharePoint migration tests"""

    azure_container_info: ClassVar[Optional[ProvisionedTemporaryAzureContainerInfo]] = None

    def test_01_provision_temporary_azure_container(self):
        """Provision a temporary Azure container"""
        result = self.client.site.provision_temporary_azure_container().execute_query()
        self.assertTrue(result.value)
        TestMigration.azure_container_info = result.value

    def test_02_get_migration_center_storage(self):
        """Get migration center storage"""
        from office365.sharepoint.migrationcenter.service.storage import (
            MigrationCenterStorage,
        )

        result = MigrationCenterStorage(self.client).get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_03_get_copy_job_progress(self):
        """Get copy job progress"""
        result = self.client.site.get_copy_job_progress().execute_query()
        self.assertIsNotNone(result.value)
