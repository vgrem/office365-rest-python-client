"""
Tenant-scope pre-migration assessment (the TENANT container walker).

Enumerates **all site collections** through the SharePoint Online tenant admin
API and runs every enabled SITE-container scan from ``assessment.registry``
against each site's property bag — e.g. the SMAT ``LargeSites`` and
``LockedSites`` reports across the whole tenant, without per-site web-tree
enumeration. Mirrors SMAT's farm-level scan: the site list comes from the
tenant first, then each site collection is checked.

Requires SharePoint admin access (``SPO.Tenant`` read). Use
``ClientContext(admin_site_url)`` + ``Tenant(ctx)``.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Optional

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.registry import active_scan_pairs
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    ScanTarget,
    SiteScanSummary,
)
from office365.runtime.client_result import ClientResult
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.runtime.operations import Progress
    from office365.sharepoint.tenant.administration.tenant import Tenant


def _coerce_int(value) -> Optional[int]:
    try:
        return int(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _clean_modified(value) -> Optional[datetime]:
    """Drop the naive ``datetime.min`` sentinel (unset) without comparing aware vs naive."""
    if value is None:
        return None
    if value.tzinfo is None and value == datetime.min:
        return None
    return value


class MigrationTenantAssessor(Entity):
    """Tenant-scope assessment driven by the ``SPO.Tenant`` site-property bag."""

    def __init__(self, tenant: "Tenant", options: Optional[AssessmentOptions] = None) -> None:
        super().__init__(tenant.context)
        self._tenant = tenant
        self._options = options or AssessmentOptions()

    def assess(
        self,
        progress: Optional[Callable[["Progress"], None]] = None,
    ) -> ClientResult[AssessmentReport]:
        """Enumerate all site collections and run the SITE-container scans.

        Args:
            progress: Optional hook fired per site collection as it is checked.
        """
        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport())
        report = return_type.value
        report.scan_id = str(uuid.uuid4())

        site_scans = [
            scanner
            for definition, scanner in active_scan_pairs(self._options, tenant_scope=True)
            if definition.container is ScanContainer.SITE
        ]
        done = {"count": 0}

        def _progress() -> None:
            done["count"] += 1
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=done["count"], total=None, stage="assessing"))

        def _on_site_properties(sites) -> None:
            for site in sites:
                props = site.properties
                size_mb = props.get("StorageUsageCurrent")  # tenant API, MB — not in the model
                summary = SiteScanSummary(
                    site_id=props.get("SiteId"),
                    site_url=site.url,
                    owner=site.owner_login_name,
                    storage_bytes=int(float(size_mb) * 1024 * 1024) if size_mb is not None else None,
                    web_count=_coerce_int(site.webs_count) or 0,
                    last_modified=_clean_modified(site.last_content_modified_date),
                    lock_state=site.lock_state,
                    report_impacted_only=True,
                )
                target = ScanTarget(ScanContainer.SITE, summary, site.url or "")
                for scan in site_scans:
                    scan.run(target, report)
                _progress()

        def _fail(e: Exception) -> None:
            report.issues.append(AssessmentIssue("warning", "access", "tenant", f"skipped — {e}"))

        self._tenant.get_site_properties_from_sharepoint_by_filters("", None, False).on_error(_fail).after_execute(
            _on_site_properties
        )

        def _finalize() -> None:
            for scan in site_scans:
                if not scan.records:
                    continue
                scan.records.sort(key=lambda r: getattr(r, "SizeInGB", 0) or 0, reverse=True)
                report._scan_reports[scan.scan_name] = ScanReport(
                    name=scan.scan_name,
                    container=ScanContainer.SITE,
                    columns=scan.columns,
                    records=scan.records,
                )

        report.attach_finalizer(_finalize)
        return return_type
