"""
Pre-migration assessment — surface blockers and warnings before touching data.

Follows deferred execution pattern and dispatches to modular scanners
(``assessment/scanners/``). List-level issue scanners (sites, fields, paths,
files, permissions) inspect loaded data, while SMAT-style scans registered in
``assessment/registry.py`` (e.g. LargeSites) collect their own data via event
hooks and emit detail reports::

    from office365.migration import MigrationAssessor

    report = MigrationAssessor(ctx.web)\
        .include_permissions()\
        .execute_query()

    print(report.summary())
    print(report.blockers)
    print(report.scan_reports["LargeSites"].records)
"""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Callable, Dict, Optional

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.registry import SCANS
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.migration.assessment.scanners import (
    AssessmentOptions,
    FieldScanner,
    FileScanner,
    PathScanner,
    PermissionScanner,
)
from office365.runtime.client_result import ClientResult
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.runtime.operations import Progress
    from office365.sharepoint.webs.web import Web

_ISSUE_SCANNERS: Dict[str, type] = {
    "fields": FieldScanner,
    "paths": PathScanner,
    "files": FileScanner,
    "permissions": PermissionScanner,
}


class MigrationAssessor(Entity):
    """
    Pre-migration assessment. Surfaces blockers and warnings before
    any data is moved.

    Example::

        report = MigrationAssessor(ctx.web)\
            .include_permissions()\
            .execute_query()

    """

    def __init__(self, web: "Web", options: AssessmentOptions | None = None) -> None:
        super().__init__(web.context)
        self._web = web
        self._options = options or AssessmentOptions()

    # ── Configuration ────────────────────────────────────────────

    def include_permissions(self) -> "MigrationAssessor":
        """Include unique permissions scan (expensive — many API calls)."""
        self._options.disabled_scans.discard("permissions")
        return self

    def include_site_admins(self) -> "MigrationAssessor":
        """Include site collection administrators in the LargeSites report."""
        self._options.include_site_admins = True
        return self

    def include_versions(self) -> "MigrationAssessor":
        """Include version history in size estimates."""
        return self

    def skip_path_checks(self) -> "MigrationAssessor":
        self._options.disabled_scans.add("paths")
        return self

    def skip_field_checks(self) -> "MigrationAssessor":
        self._options.disabled_scans.add("fields")
        return self

    def enable_scan(self, name: str) -> "MigrationAssessor":
        """Re-enable a scan disabled in options (SMAT ScanDef ``Enabled``)."""
        self._options.disabled_scans.discard(name)
        return self

    def disable_scan(self, name: str) -> "MigrationAssessor":
        """Disable a scan — its data is not collected (SMAT ScanDef ``Enabled``)."""
        self._options.disabled_scans.add(name)
        return self

    # ── Execution ─────────────────────────────────────────────────

    def assess(
        self,
        progress: Optional[Callable[["Progress"], None]] = None,
        recursive: bool = True,
    ) -> ClientResult[AssessmentReport]:
        """Run the assessment — the whole web tree (site + subsites) by default.

        Lists that can't be read (unique permissions, protected system lists, or
        an unreachable site) are skipped with a warning instead of aborting the
        whole scan — an assessor must report, not crash.

        Args:
            progress: Optional hook invoked once per list as its scan completes
              (``done`` = lists scanned in the current web, ``total`` = that
              web's list count, ``items`` = the list just scanned).
            recursive: Whether to scan subsites (default True).
        """

        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport())
        report = return_type.value
        report.scan_id = str(uuid.uuid4())

        # List-level issue scanners (enabled unless disabled in options)
        scanners = {
            name: cls(self._options) for name, cls in _ISSUE_SCANNERS.items() if name not in self._options.disabled_scans
        }
        # SMAT-style report scans (registry, ScanDef-aware)
        report_pairs = [
            (d, d.scanner(self._options)) for d in SCANS if d.enabled and d.name not in self._options.disabled_scans
        ]
        report_scans = [s for _, s in report_pairs]
        all_scanners = list(scanners.values()) + report_scans

        needs_collection = any(s.needs_collection for s in report_scans)
        needs_list_metadata = any(s.needs_list_metadata for s in report_scans)
        needs_webs = any(s.needs_webs for s in report_scans)

        def _flag_failure(location: str, error: Exception) -> None:
            self._flag_access(report, location, error)

        def _assess_web(web) -> None:
            """Queue the list scan for one web (root or subsite)."""
            prefix = (web.url or "").rstrip("/")
            query = web.lists.get()
            if needs_list_metadata:
                query = query.select(["Id", "Title", "Hidden", "ItemCount", "LastItemModifiedDate"])
            query.on_error(lambda e, loc=f"{prefix}/web/lists": _flag_failure(loc, e)).after_execute(
                lambda lists: self._scan_web_lists(
                    lists,
                    prefix=prefix,
                    report=report,
                    scanners=scanners,
                    report_scans=report_scans,
                    needs_list_metadata=needs_list_metadata,
                    progress=progress,
                    flag_failure=_flag_failure,
                )
            )

        def _scan_webs_tree(webs) -> None:
            report.total_webs = len(webs)
            if needs_webs:
                for s in report_scans:
                    s.on_webs(webs, report)
            for web in webs:
                _assess_web(web)

        # site collection metadata (usage/storage, owner) for collection-level scans
        if needs_collection:
            site = self._web.context.site
            (
                site.select(["Id", "Url", "UsageInfo", "Owner/Title", "Owner/Email"])
                .expand(["Owner"])
                .get()
                .on_error(lambda e: _flag_failure("web", e))
                .after_execute(
                    lambda site: [s.on_collection(site, report) for s in report_scans],
                )
            )

        _assess_web(self._web)
        if recursive:
            self._web.get_all_webs(progress=progress).on_error(lambda e: _flag_failure("web/webs", e)).after_execute(
                _scan_webs_tree
            )
        else:
            self._web.webs.get().on_error(lambda e: _flag_failure("web/webs", e)).after_execute(
                lambda webs: setattr(report, "total_webs", len(webs))
            )

        # Once the deferred batch has settled, each scan assembles its detail
        # report — the report triggers this lazily on first consumption.
        def _finalize() -> None:
            for s in all_scanners:
                s.finalize(report)
            for definition, s in report_pairs:
                if s.records:
                    report._scan_reports[s.scan_name] = ScanReport(
                        name=s.scan_name,
                        category=definition.category,
                        columns=s.columns,
                        records=s.records,
                    )

        report.attach_finalizer(_finalize)
        return return_type

    def _flag_access(self, report: AssessmentReport, location: str, error: Exception) -> None:
        """Record an access warning — an unreadable area is skipped, not fatal."""
        if location.endswith("web/webs"):
            report.webs_skipped = True
        elif location.endswith("web/lists"):
            report.lists_skipped = True
        report.issues.append(AssessmentIssue("warning", "access", location, f"skipped — {error}"))

    def _scan_web_lists(
        self,
        lists,
        prefix: str,
        report: AssessmentReport,
        scanners: dict,
        report_scans: list,
        needs_list_metadata: bool,
        progress: Optional[Callable[["Progress"], None]],
        flag_failure: Callable,
    ) -> None:
        """Scan one web's lists — dispatch fields/items to the issue scanners."""
        report.total_lists += len(lists)
        if needs_list_metadata:
            for s in report_scans:
                s.on_lists(lists, report)
        total = len(lists)
        completed = {"count": 0}

        def _progress(lst) -> None:
            completed["count"] += 1
            if callable(progress):
                from office365.runtime.operations import Progress

                progress(Progress(done=completed["count"], total=total, stage="assessing", items=[lst]))

        for lst in lists:
            if lst.hidden:
                _progress(lst)
                continue
            location = f"{prefix}/lists/{lst.title}"
            pending = {"count": 0}

            def _scan_done(lst=lst, pending=pending) -> None:
                pending["count"] -= 1
                if pending["count"] <= 0:
                    _progress(lst)

            def _fail(e, loc=location, lst=lst, done=_scan_done) -> None:
                flag_failure(loc, e)
                done(lst)

            if "fields" in scanners:
                pending["count"] += 1
                lst.fields.get().on_error(_fail).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        scanners["fields"].on_fields(col, report, location=loc),
                        done(lst),
                    )
                )
            if "paths" in scanners or "files" in scanners:
                pending["count"] += 1
                lst.items.select(["FileRef", "FileLeafRef", "File/Length"]).expand(["File"]).get().on_error(
                    _fail
                ).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        self._scan_items(scanners, col, report, location=loc),
                        done(lst),
                    )
                )
            if "permissions" in scanners:
                pending["count"] += 1
                (
                    lst.items.select(["HasUniqueRoleAssignments", "FileRef"])
                    .get_all()
                    .on_error(_fail)
                    .after_execute(
                        lambda col, lst=lst, loc=location, done=_scan_done: (
                            scanners["permissions"].on_items(col, report, location=loc),
                            done(lst),
                        )
                    )
                )
            if pending["count"] == 0:  # no sub-scans enabled
                _progress(lst)

    @staticmethod
    def _scan_items(scanners: dict, items, report: AssessmentReport, location: str) -> None:
        """Accumulate the file inventory, then run the path/file scanners."""
        for item in items:
            report.total_files += 1
            report.total_size_gb += (item.file.length or 0) / 1024 / 1024 / 1024
        if "paths" in scanners:
            scanners["paths"].on_items(items, report, location)
        if "files" in scanners:
            scanners["files"].on_items(items, report, location)
