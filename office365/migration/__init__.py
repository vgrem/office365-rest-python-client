"""Migration toolkit — SPMT-style, resumable, client-side migrations.

The toolkit composes the client (SharePoint v1 / Graph) with a data pipeline to
move items between source and target adapters with checkpoints, resumption, and
verification.

Quick start (filesystem -> filesystem):

    from office365.migration import MigrationJob
    from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget

    job = MigrationJob(FileSystemSource("src"), FileSystemTarget("dst"))
    job.plan()
    job.run()
    print(job.stats.summary())
    print(job.verify().summary())
"""

from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessor import MigrationAssessor
from office365.migration.base import (
    ConflictResolution,
    ExportFormat,
    ItemStatus,
    MigrationItem,
    MigrationMode,
    MigrationOptions,
    MigrationPhase,
    MigrationStats,
)
from office365.migration.checkpoint import Checkpoint
from office365.migration.job import MigrationJob
from office365.migration.manifest import Manifest
from office365.migration.report import MigrationReport, build_report, export_reports
from office365.migration.runner import MigrationRunner
from office365.migration.server_job import MigrationServerJob
from office365.migration.validators import VerificationReport, verify

__all__ = [
    "AssessmentReport",
    "Checkpoint",
    "ConflictResolution",
    "ExportFormat",
    "ItemStatus",
    "Manifest",
    "MigrationAssessor",
    "MigrationItem",
    "MigrationJob",
    "MigrationMode",
    "MigrationOptions",
    "MigrationPhase",
    "MigrationReport",
    "MigrationRunner",
    "MigrationServerJob",
    "MigrationStats",
    "VerificationReport",
    "build_report",
    "export_reports",
    "verify",
]
