"""
Tenant-scope pre-migration assessment.

Enumerates **all site collections** through the SharePoint Online tenant admin
API and runs the SPSite-category scans against the site-property bag — e.g. the
SMAT ``LargeSites-detail`` report across the whole tenant, without per-site
web-tree enumeration.

Mirrors SMAT's farm-level scan: the site list comes from the tenant first, then
each site collection is checked against the scan criteria.

Requires SharePoint admin access (``SPO.Tenant`` read) — SMAT's farm-account
prerequisite. Use ``ClientContext(admin_site_url)`` + ``Tenant(ctx)``.
"""

from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Callable, Optional

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scan_category import ScanCategory
from office365.migration.assessment.scanners import AssessmentOptions
from office365.migration.assessment.scanners.large_sites import (
    LargeSitesScanner,
    build_large_site_record,
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
        """Enumerate all site collections and run the tenant scans.

        Args:
            progress: Optional hook fired per site collection as it is checked.
        """
        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport())
        report = return_type.value
        report.scan_id = str(uuid.uuid4())

        scanner = LargeSitesScanner(self._options)
        done = {"count": 0}

        def _progress() -> None:
            done["count"] += 1
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=done["count"], total=None, stage="assessing"))

        def _on_site_properties(sites) -> None:
            for site in sites:
                # locked / no-access sites are skipped (SMAT behavior)
                if site.lock_state and site.lock_state != "Unlock":
                    _progress()
                    continue
                # SiteId / StorageUsageCurrent are returned by the tenant API but
                # not part of the generated SiteProperties model — read the raw bag
                size_mb = site.properties.get("StorageUsageCurrent")
                # SMAT reports site collections *over* 500 GB
                if size_mb is None or size_mb / 1024 <= self._options.large_site_threshold_gb:
                    _progress()
                    continue
                scanner.records.append(
                    build_large_site_record(
                        site_id=site.properties.get("SiteId"),
                        site_url=site.url,
                        site_owner=site.owner_login_name,
                        size_mb=float(size_mb),
                        num_of_webs=_coerce_int(site.webs_count),
                        last_modified=_clean_modified(site.last_content_modified_date),
                        scan_id=report.scan_id,
                    )
                )
                _progress()

        def _fail(e: Exception) -> None:
            report.issues.append(AssessmentIssue("warning", "access", "tenant", f"skipped — {e}"))

        self._tenant.get_site_properties_from_sharepoint_by_filters("", None, False).on_error(_fail).after_execute(
            _on_site_properties
        )

        def _finalize() -> None:
            if scanner.records:
                scanner.records.sort(key=lambda r: r.SizeInGB or 0, reverse=True)
                report._scan_reports[scanner.scan_name] = ScanReport(
                    name=scanner.scan_name,
                    category=ScanCategory.SPSITE,
                    columns=scanner.columns,
                    records=scanner.records,
                )

        report.attach_finalizer(_finalize)
        return return_type
