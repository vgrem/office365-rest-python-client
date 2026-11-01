from __future__ import annotations

import time
from typing import ClassVar, Optional
from uuid import uuid4

from office365.sharepoint.sites.azure_container_Info import (
    ProvisionedTemporaryAzureContainerInfo,
)
from office365.sharepoint.sites.copy_job_progress import CopyJobProgress
from office365.sharepoint.sites.copy_migration_iInfo import CopyMigrationInfo
from office365.sharepoint.sites.migration.copyoptions import CopyMigrationOptions
from office365.sharepoint.sites.site import Site

from tests.decorators import requires_call
from tests.sharepoint.sharepoint_case import SPTestCase

# A copy job is queued, so the progress read right after the call may still be empty.
_COPY_JOB_ATTEMPTS = 20
_COPY_JOB_PAUSE = 3


class TestMigration(SPTestCase):
    """SharePoint migration tests"""

    azure_container_info: ClassVar[Optional[ProvisionedTemporaryAzureContainerInfo]] = None

    @requires_call(Site.provision_temporary_azure_container, flow="application")
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

    @requires_call(Site.create_copy_jobs, Site.get_copy_job_progress, flow="application")
    def test_03_get_copy_job_progress(self):
        """A queued copy job reports what happened to it"""
        library = self.client.web.get_folder_by_server_relative_url("Shared Documents").execute_query()
        suffix = uuid4().hex[:8]
        source = library.upload_file(f"copy_job_{suffix}.txt", b"copy job source").execute_query()
        target = library.folders.add(f"copy_job_target_{suffix}").execute_query()
        try:
            jobs = (
                self.client.site.create_copy_jobs(
                    [source.server_relative_url],
                    target.server_relative_url,
                    CopyMigrationOptions(),
                )
                .execute_query()
                .value
            )
            self.assertTrue(jobs, "the service queued no copy job for the export")
            job = jobs[0]
            self.assertTrue(job.JobId, "a queued job has an id")
            self.assertIn("queue.core.windows.net", job.JobQueueUri or "")

            logs = "".join(self._wait_for_copy_job(job).Logs)
            self.assertIn(job.JobId, logs, "progress belongs to the job it was asked about")
            self.assertIn("JobEnd", logs, "the job reached an end state")
        finally:
            target.delete_object().execute_query()
            source.delete_object().execute_query()

    def _wait_for_copy_job(self, job: CopyMigrationInfo) -> CopyJobProgress:
        """Polls the job until it leaves the queue.

        Args:
            job (CopyMigrationInfo): The job ``create_copy_jobs`` returned.
        """
        for _ in range(_COPY_JOB_ATTEMPTS):
            progress: CopyJobProgress = self.client.site.get_copy_job_progress(job).execute_query().value
            if "JobEnd" in "".join(progress.Logs):
                return progress
            time.sleep(_COPY_JOB_PAUSE)
        self.fail("the copy job did not reach a terminal state")
