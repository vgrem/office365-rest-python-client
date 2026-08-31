"""
Pre-migration assessment — surface blockers and warnings before touching data.

Follows deferred execution pattern and dispatches to modular scanners
(``assessment/scanners/``), one per concern — sites, fields, paths, files,
permissions::

    from office365.migration import MigrationAssessor

    report = MigrationAssessor(ctx.web)\
        .include_permissions()\
        .include_versions()\
        .execute_query()

    print(report.summary())
    print(report.blockers)
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Dict, Optional

from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport
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
        self._enabled: Dict[str, bool] = {
            "paths": True,
            "fields": True,
            "files": True,
            "permissions": False,
        }

    # ── Configuration ────────────────────────────────────────────

    def include_permissions(self) -> "MigrationAssessor":
        """Include unique permissions scan (expensive — many API calls)."""
        self._enabled["permissions"] = True
        return self

    def include_versions(self) -> "MigrationAssessor":
        """Include version history in size estimates."""
        return self

    def skip_path_checks(self) -> "MigrationAssessor":
        self._enabled["paths"] = False
        return self

    def skip_field_checks(self) -> "MigrationAssessor":
        self._enabled["fields"] = False
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

        scanners = {
            "fields": FieldScanner(self._options),
            "paths": PathScanner(self._options),
            "files": FileScanner(self._options),
            "permissions": PermissionScanner(self._options),
        }

        def _flag_failure(location: str, error: Exception) -> None:
            report = return_type.value
            if location.endswith("web/webs"):
                report.webs_skipped = True
            elif location.endswith("web/lists"):
                report.lists_skipped = True
            self._flag(report, "warning", "access", location, f"skipped — {error}")

        def _assess_web(web) -> None:
            """Queue the list scan for one web (root or subsite)."""
            prefix = (web.url or "").rstrip("/")

            def _scan_web_lists(lists) -> None:
                report = return_type.value
                report.total_lists += len(lists)
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
                        _flag_failure(loc, e)
                        done(lst)

                    if self._enabled["fields"]:
                        pending["count"] += 1
                        lst.fields.get().on_error(_fail).after_execute(
                            lambda col, lst=lst, loc=location, done=_scan_done: (
                                scanners["fields"].run(col, report, location=loc),
                                done(lst),
                            )
                        )
                    if self._enabled["paths"] or self._enabled["files"]:
                        pending["count"] += 1
                        lst.items.select(["FileRef", "FileLeafRef", "File/Length"]).expand(["File"]).get().on_error(
                            _fail
                        ).after_execute(
                            lambda col, lst=lst, done=_scan_done: (
                                self._scan_items(scanners, col, report),
                                done(lst),
                            )
                        )
                    if self._enabled["permissions"]:
                        pending["count"] += 1
                        (
                            lst.items.select(["HasUniqueRoleAssignments", "FileRef"])
                            .get_all()
                            .on_error(_fail)
                            .after_execute(
                                lambda col, lst=lst, loc=location, done=_scan_done: (
                                    scanners["permissions"].run(col, report, location=loc),
                                    done(lst),
                                )
                            )
                        )
                    if pending["count"] == 0:  # no sub-scans enabled
                        _progress(lst)

            web.lists.get().on_error(lambda e, loc=f"{prefix}/web/lists": _flag_failure(loc, e)).after_execute(
                _scan_web_lists
            )

        def _scan_webs_tree(webs) -> None:
            return_type.value.total_webs = len(webs)
            for web in webs:
                _assess_web(web)

        _assess_web(self._web)
        if recursive:
            self._web.get_all_webs(progress=progress).on_error(lambda e: _flag_failure("web/webs", e)).after_execute(
                _scan_webs_tree
            )
        else:
            self._web.webs.get().on_error(lambda e: _flag_failure("web/webs", e)).after_execute(
                lambda webs: setattr(return_type.value, "total_webs", len(webs))
            )
        return return_type

    def _flag(
        self,
        report: AssessmentReport,
        severity: str,
        category: str,
        location: str,
        message: str,
        suggestion: str = "",
    ) -> None:
        report.issues.append(AssessmentIssue(severity, category, location, message, suggestion))

    @staticmethod
    def _scan_items(scanners: dict, items, report: AssessmentReport) -> None:
        """Accumulate the file inventory, then run the path/file scanners."""
        for item in items:
            report.total_files += 1
            report.total_size_gb += (item.file.length or 0) / 1024 / 1024 / 1024
        scanners["paths"].run(items, report)
        scanners["files"].run(items, report)
