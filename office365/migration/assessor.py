"""
Pre-migration assessment — surface blockers and warnings before touching data.

Follows deferred execution pattern. A **walker** loads each SharePoint container
once (site, web tree, lists, and per list: fields, items) and dispatches the
payload to every scan registered for that container — each scan implements one
method, :meth:`BaseScanner.run`::

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
    from office365.sharepoint.webs.web import Web


def _scan_for(active, container: ScanContainer, items_load: Optional[str] = None):
    """Scans registered for a container (optionally an items projection)."""
    return [s for d, s in active if d.container is container and (items_load is None or s.items_load == items_load)]


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

        active = active_scan_pairs(self._options)
        site_scans = _scan_for(active, ScanContainer.SITE)
        fields_scans = _scan_for(active, ScanContainer.FIELDS)
        items_scans = _scan_for(active, ScanContainer.ITEMS, "default")
        unique_items_scans = _scan_for(active, ScanContainer.ITEMS, "unique")

        # SITE scans aggregate the site collection -> summary drives the loads
        needs_site = bool(site_scans)
        needs_list_metadata = needs_site  # item counts / last-modified for the summary
        summary = SiteScanSummary()

        def _dispatch(container: ScanContainer, scans, entity, location: str) -> None:
            target = ScanTarget(container=container, entity=entity, location=location)
            for scan in scans:
                scan.run(target, report)

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
                    summary=summary,
                    fields_scans=fields_scans,
                    items_scans=items_scans,
                    unique_items_scans=unique_items_scans,
                    needs_list_metadata=needs_list_metadata,
                    progress=progress,
                    flag_failure=_flag_failure,
                    dispatch=_dispatch,
                )
            )

        def _scan_webs_tree(webs) -> None:
            report.total_webs = len(webs)
            if needs_site:
                summary.web_count = len(webs)
            for web in webs:
                _assess_web(web)

        # site collection metadata (usage/storage, owner) for SITE-container scans
        if needs_site:
            site = self._web.context.site
            (
                site.select(["Id", "Url", "UsageInfo", "Owner/Title", "Owner/Email"])
                .expand(["Owner"])
                .get()
                .on_error(lambda e: _flag_failure("web", e))
                .after_execute(
                    lambda site: self._on_site_loaded(site, report, summary, site_scans, needs_site),
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

        # Once the deferred batch has settled, SITE scans assemble their rows
        # from the aggregated summary — the report triggers this lazily.
        def _finalize() -> None:
            for definition, scanner in active:
                if definition.container is ScanContainer.SITE:
                    scanner.run(ScanTarget(ScanContainer.SITE, summary, summary.site_url or ""), report)
            for definition, scanner in active:
                if scanner.records:
                    report._scan_reports[scanner.scan_name] = ScanReport(
                        name=scanner.scan_name,
                        container=definition.container,
                        columns=scanner.columns,
                        records=scanner.records,
                    )

        report.attach_finalizer(_finalize)
        return return_type

    def _on_site_loaded(
        self,
        site,
        report: AssessmentReport,
        summary: SiteScanSummary,
        site_scans,
        needs_site: bool,
    ) -> None:
        """Site collection metadata is ready — populate the summary for SITE scans."""
        summary.site_id = site.id
        summary.site_url = site.url
        usage = site.properties.get("UsageInfo")
        if usage is not None:
            summary.storage_bytes = getattr(usage, "Storage", None)
            summary.hits = getattr(usage, "Hits", None)
        owner = site.properties.get("Owner")
        if owner is not None:
            title = owner.properties.get("Title") or owner.properties.get("LoginName")
            if title:
                summary.owner = title
        if needs_site and self._options.include_site_admins:
            site.root_web.associated_owner_group.users.get().on_error(lambda e: None).after_execute(
                lambda users: self._set_site_admins(summary, users)
            )

    @staticmethod
    def _set_site_admins(summary: SiteScanSummary, users) -> None:
        logins = [
            u.properties.get("LoginName") or u.properties.get("Title")
            for u in users
            if u.properties.get("LoginName") or u.properties.get("Title")
        ]
        if logins:
            summary.admins = "; ".join(logins)

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
        summary: SiteScanSummary,
        fields_scans,
        items_scans,
        unique_items_scans,
        needs_list_metadata: bool,
        progress: Optional[Callable[["Progress"], None]],
        flag_failure: Callable,
        dispatch,
    ) -> None:
        """Scan one web's lists — load each list's sub-resources and dispatch by container."""
        report.total_lists += len(lists)
        if needs_list_metadata:
            for lst in lists:
                count = lst.item_count
                if isinstance(count, int):
                    summary.item_count += count
                modified = lst.last_item_modified_date
                if modified is not None and (summary.last_modified is None or modified > summary.last_modified):
                    summary.last_modified = modified
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

            if fields_scans:
                pending["count"] += 1
                lst.fields.get().on_error(_fail).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        dispatch(ScanContainer.FIELDS, fields_scans, col, loc),
                        done(lst),
                    )
                )
            if items_scans:
                pending["count"] += 1
                lst.items.select(["FileRef", "FileLeafRef", "File/Length"]).expand(["File"]).get().on_error(
                    _fail
                ).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        self._scan_items(items_scans, col, report, loc, dispatch),
                        done(lst),
                    )
                )
            if unique_items_scans:
                pending["count"] += 1
                (
                    lst.items.select(["HasUniqueRoleAssignments", "FileRef"])
                    .get_all()
                    .on_error(_fail)
                    .after_execute(
                        lambda col, lst=lst, loc=location, done=_scan_done: (
                            dispatch(ScanContainer.ITEMS, unique_items_scans, col, loc),
                            done(lst),
                        )
                    )
                )
            if pending["count"] == 0:  # no sub-scans enabled
                _progress(lst)

    @staticmethod
    def _scan_items(items_scans, items, report: AssessmentReport, location: str, dispatch) -> None:
        """Accumulate the file inventory, then run the item-level scanners."""
        for item in items:
            report.total_files += 1
            report.total_size_gb += (item.file.length or 0) / 1024 / 1024 / 1024
        dispatch(ScanContainer.ITEMS, items_scans, items, location)
