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

from collections.abc import Callable
from datetime import datetime
from typing import TYPE_CHECKING

from office365.migration._util import coerce_int, emit_progress
from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.runner import ScanRunner
from office365.migration.assessment.scanners import AssessmentOptions
from office365.migration.sharepoint.registry import sharepoint_scan_pairs
from office365.migration.sharepoint.scanners.summary import SiteScanSummary
from office365.runtime.client_result import ClientResult
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.runtime.operations import Progress
    from office365.sharepoint.tenant.administration.tenant import Tenant


def _clean_modified(value) -> datetime | None:
    """Drop the naive ``datetime.min`` sentinel (unset) without comparing aware vs naive."""
    if value is None:
        return None
    if value.tzinfo is None and value == datetime.min:
        return None
    return value


class MigrationTenantAssessor(Entity):
    """Tenant-scope assessment driven by the ``SPO.Tenant`` site-property bag."""

    def __init__(self, tenant: "Tenant", options: AssessmentOptions | None = None) -> None:
        super().__init__(tenant.context)
        self._tenant = tenant
        self._options = options or AssessmentOptions()

    def assess(
        self,
        progress: Callable[["Progress"], None] | None = None,
    ) -> ClientResult[AssessmentReport]:
        """Enumerate all site collections and run the SITE-container scans.

        Args:
            progress: Optional hook fired per site collection as it is checked.
        """
        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport.new())
        runner = ScanRunner(sharepoint_scan_pairs(self._options, tenant_scope=True), report=return_type.value)
        report = runner.report
        done = {"count": 0}

        def _progress() -> None:
            done["count"] += 1
            emit_progress(progress, done=done["count"], stage="assessing")

        def _on_site_properties(sites) -> None:
            for site in sites:
                props = site.properties
                storage = props.get("StorageUsage")  # SiteProperties.StorageUsage — bytes
                summary = SiteScanSummary(
                    site_id=props.get("SiteId"),
                    site_url=site.url,
                    owner=site.owner_login_name,
                    storage_bytes=int(storage) if storage is not None else None,
                    web_count=coerce_int(site.webs_count) or 0,
                    last_modified=_clean_modified(site.last_content_modified_date),
                    lock_state=site.lock_state,
                    report_impacted_only=True,
                )
                runner.dispatch(ScanContainer.SITE, summary, site.url or "")
                _progress()

        self._tenant.get_site_properties_from_sharepoint_by_filters("", None, include_detail=True).on_error(
            lambda e: runner.flag_access("tenant", e)
        ).after_execute(_on_site_properties)

        report.attach_finalizer(runner.collect)
        return return_type
