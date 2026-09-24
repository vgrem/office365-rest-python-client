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
    print(report.scan_report(LargeSitesScanner).records)
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from office365.migration.assessment.containers import ScanContainer
from office365.migration.assessment.issue import AssessmentIssue
from office365.migration.assessment.report import AssessmentReport
from office365.migration.assessment.runner import ScanRunner
from office365.migration.assessment.scanners import AssessmentOptions
from office365.migration.sharepoint.adapters import is_taxonomy_validation
from office365.migration.sharepoint.options import SharePointAssessmentOptions
from office365.migration.sharepoint.registry import sharepoint_scan_pairs
from office365.migration.sharepoint.scanners.summary import SiteScanSummary
from office365.runtime.client_result import ClientResult
from office365.runtime.operations import emit_progress
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.runtime.operations import Progress
    from office365.sharepoint.sites.site import Site
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
        self._options = options or SharePointAssessmentOptions()

    # ── Configuration ────────────────────────────────────────────

    def include_permissions(self) -> "MigrationAssessor":
        """Include unique permissions scan (expensive — many API calls)."""
        self._options.disabled_scans.discard("permissions")
        return self

    def include_site_admins(self) -> "MigrationAssessor":
        """Include site collection administrators in the LargeSites report."""
        self._options.include_site_admins = True
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
        progress: Callable[["Progress"], None] | None = None,
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
        return_type = ClientResult[AssessmentReport](self.context, AssessmentReport.new())
        runner = ScanRunner(sharepoint_scan_pairs(self._options), report=return_type.value)
        report = runner.report

        needs_site = bool(runner.scanners(ScanContainer.SITE))
        # item counts / last-modified feed the SITE summary and the LIST-container scans
        needs_list_metadata = needs_site or bool(runner.scanners(ScanContainer.LIST))
        summary = SiteScanSummary()

        def _flag_failure(location: str, error: Exception) -> None:
            self._flag_access(runner, location, error)

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
                    runner=runner,
                    summary=summary,
                    needs_list_metadata=needs_list_metadata,
                    progress=progress,
                    flag_failure=_flag_failure,
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
                .after_execute(lambda site: self._on_site_loaded(site, summary, needs_site))
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
            runner.run_site_scans(summary)
            runner.collect()

        report.attach_finalizer(_finalize)
        return return_type

    def _on_site_loaded(self, site: Site, summary: SiteScanSummary, needs_site: bool) -> None:
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

    @staticmethod
    def _flag_access(runner: ScanRunner, location: str, error: Exception) -> None:
        """Record a warning for an area that could not be read (skipped, not fatal).

        A Managed Metadata column pointing to a deleted term set fails the list
        read with ``SPFieldValidationException`` — surface it as a dedicated
        ``taxonomy`` issue so the report names the cause and the fix.
        """
        report = runner.report
        if location.endswith("web/webs"):
            report.webs_skipped = True
        elif location.endswith("web/lists"):
            report.lists_skipped = True
        if is_taxonomy_validation(error):
            report.issues.append(
                AssessmentIssue(
                    "warning",
                    "taxonomy",
                    location,
                    f"list read failed — a Managed Metadata column references a missing term set ({error})",
                    "Fix the column or export the list without taxonomy fields (SharePointListSource "
                    "auto-fallback excludes them)",
                )
            )
            return
        runner.flag_access(location, error)

    def _scan_web_lists(
        self,
        lists,
        prefix: str,
        runner: ScanRunner,
        summary: SiteScanSummary,
        needs_list_metadata: bool,
        progress: Callable[["Progress"], None] | None,
        flag_failure: Callable,
    ) -> None:
        """Scan one web's lists — load each list's sub-resources and dispatch by container."""
        report = runner.report
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

        has_fields = bool(runner.scanners(ScanContainer.FIELDS))
        has_items = bool(runner.scanners(ScanContainer.ITEMS, "default"))
        has_unique_items = bool(runner.scanners(ScanContainer.ITEMS, "unique"))
        has_list = bool(runner.scanners(ScanContainer.LIST))

        def _progress(lst) -> None:
            completed["count"] += 1
            emit_progress(progress, done=completed["count"], total=total, stage="assessing", items=[lst])

        for lst in lists:
            location = f"{prefix}/lists/{lst.title}"
            if has_list:
                runner.dispatch(ScanContainer.LIST, lst, location)
            if lst.hidden:
                _progress(lst)
                continue
            pending = {"count": 0}

            def _scan_done(lst=lst, pending=pending) -> None:
                pending["count"] -= 1
                if pending["count"] <= 0:
                    _progress(lst)

            def _fail(e, loc=location, lst=lst, done=_scan_done) -> None:
                flag_failure(loc, e)
                done(lst)

            if has_fields:
                pending["count"] += 1
                lst.fields.get().on_error(_fail).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        runner.dispatch(ScanContainer.FIELDS, col, loc),
                        done(lst),
                    )
                )
            if has_items:
                pending["count"] += 1
                lst.items.select(
                    ["FileRef", "FileLeafRef", "File/Length", "File/MajorVersion", "File/MinorVersion"]
                ).expand(["File"]).get().on_error(_fail).after_execute(
                    lambda col, lst=lst, loc=location, done=_scan_done: (
                        self._scan_items(runner, col, loc),
                        done(lst),
                    )
                )
            if has_unique_items:
                pending["count"] += 1
                (
                    lst.items.select(["HasUniqueRoleAssignments", "FileRef"])
                    .get_all()
                    .on_error(_fail)
                    .after_execute(
                        lambda col, lst=lst, loc=location, done=_scan_done: (
                            runner.dispatch(ScanContainer.ITEMS, col, loc, items_load="unique"),
                            done(lst),
                        )
                    )
                )
            if pending["count"] == 0:  # no sub-scans enabled
                _progress(lst)

    @staticmethod
    def _scan_items(runner: ScanRunner, items, location: str) -> None:
        """Accumulate the file inventory, then run the item-level scanners."""
        report = runner.report
        for item in items:
            report.total_files += 1
            report.total_size_gb += (item.file.length or 0) / 1024 / 1024 / 1024
        runner.dispatch(ScanContainer.ITEMS, items, location, items_load="default")
