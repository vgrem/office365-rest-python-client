"""
Pre-migration assessment — surface blockers and warnings before moving data.

Basic usage of the modular ``MigrationAssessor``: scan the site, then print a
summary plus the flagged issues (blockers block a migration, warnings are
advisory) and the SMAT-style scan detail reports. A determinate progress bar
tracks the per-list scan.

Scans are registered in ``office365.migration.assessment.registry`` (mirroring
SMAT's ScanDef.json); ``--disable-scan`` turns one off (its data is not
collected), ``--only-scan`` runs just one.

The assessment is the "scan" phase of the migration workflow — pair it with
``MigrationJob`` (see ``migrate_files.py`` / ``export_list_to_json.py``) to
assess, then migrate, then verify.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import argparse

from office365.migration import SCANS, MigrationAssessor
from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress) -> None:
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)

    return hook


def print_scan_reports(report) -> None:
    """Print the SMAT-style detail reports (e.g. LargeSites)."""
    for name, scan in report.scan_reports.items():
        print(f"\n{name} ({scan.container.value}): {len(scan.records)} row(s)")
        for row in scan.to_records():
            print("  " + " | ".join(f"{k}={row[k]}" for k in scan.columns))


def main():
    parser = argparse.ArgumentParser(description="Assess a SharePoint site for migration readiness")
    parser.add_argument("--site-url", default=team_site_url, help="site URL to assess (scans subsites too)")
    parser.add_argument("--permissions", action="store_true", help="scan for unique permissions (slower)")
    parser.add_argument("--site-admins", action="store_true", help="include site collection admins in LargeSites")
    parser.add_argument("--no-recursive", action="store_true", help="scan only the root web, not subsites")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    parser.add_argument("--disable-scan", action="append", help="disable a scan (e.g. LargeSites)")
    parser.add_argument("--only-scan", help="run only this scan (e.g. LargeSites)")
    parser.add_argument("--output", help="directory to export AssessmentReport.csv/.json + ScannerReports/")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    assessor = MigrationAssessor(ctx.web)
    if args.permissions:
        assessor.include_permissions()
    if args.site_admins:
        assessor.include_site_admins()
    for name in args.disable_scan or []:
        assessor.disable_scan(name)
    if args.only_scan:
        for definition in SCANS:
            if definition.name != args.only_scan:
                assessor.disable_scan(definition.name)

    hook = None if args.no_progress else progress_bar("Assessing")
    report = assessor.assess(progress=hook, recursive=not args.no_recursive).execute_query().value
    print(report.summary())

    if args.output:
        from office365.migration.assessment.export import export_assessment

        written = export_assessment(report, args.output)
        print("Exported:", ", ".join(written))

    print_scan_reports(report)

    if report.blockers:
        print("\nBlockers (must fix before migrating):")
        for issue in report.blockers:
            print(f"  - [{issue.category}] {issue.location}: {issue.message}")
            if issue.suggestion:
                print(f"    -> {issue.suggestion}")
    if report.warnings:
        print("\nWarnings (advisory):")
        for issue in report.warnings:
            print(f"  - [{issue.category}] {issue.location}: {issue.message}")


if __name__ == "__main__":
    main()
