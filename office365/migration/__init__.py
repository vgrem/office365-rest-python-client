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

from office365.migration.assessment.registry import SCANS, ScanDefinition, enabled_scans, get_scan
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scan_category import ScanCategory
from office365.migration.assessment.scanners import AssessmentOptions, LargeSitesScanner
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
from office365.migration.session import MigrationSession, MigrationTask
from office365.migration.tenant_assessor import MigrationTenantAssessor
from office365.migration.validators import VerificationReport, verify

__all__ = [
    "AssessmentOptions",
    "AssessmentReport",
    "Checkpoint",
    "ConflictResolution",
    "ExportFormat",
    "ItemStatus",
    "LargeSitesScanner",
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
    "MigrationSession",
    "MigrationStats",
    "MigrationTask",
    "MigrationTenantAssessor",
    "SCANS",
    "ScanCategory",
    "ScanDefinition",
    "ScanReport",
    "VerificationReport",
    "build_report",
    "enabled_scans",
    "export_reports",
    "get_scan",
    "verify",
]
