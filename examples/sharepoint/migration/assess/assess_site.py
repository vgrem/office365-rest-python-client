"""
Pre-migration assessment — surface blockers and warnings before moving data.

Basic usage of the modular ``MigrationAssessor``: scan the site, then print a
summary plus the flagged issues (blockers block a migration, warnings are
advisory) and the SMAT-style scan detail reports.

Scans are registered in ``office365.migration.sharepoint.registry`` (mirroring
SMAT's ScanDef.json); ``--disable-scan`` turns one off (its data is not
collected), ``--only-scan`` runs just one.

The assessment is the "scan" phase of the migration workflow — pair it with
``MigrationJob`` (see ``migrate_files.py`` / ``export_list.py``) to
assess, then migrate, then verify.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import argparse
import json
import os

from office365.migration import MigrationAssessor
from office365.migration.sharepoint.registry import SHAREPOINT_SCANS
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def write_report(report, output_dir: str) -> str:
    """Write the assessment (issues + scan details) as one ``AssessmentReport.json``."""
    data = {
        "issues": report.to_records(),
        "scans": {name: scan.to_records() for name, scan in report.scan_reports.items()},
    }
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "AssessmentReport.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    return path


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
    parser.add_argument("--disable-scan", action="append", help="disable a scan (e.g. LargeSites)")
    parser.add_argument("--only-scan", help="run only this scan (e.g. LargeSites)")
    parser.add_argument("--output", default="/tmp", help="directory for the AssessmentReport.json report")
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
        for definition in SHAREPOINT_SCANS:
            if definition.name != args.only_scan:
                assessor.disable_scan(definition.name)

    print("Assessing…", flush=True)
    report = assessor.assess(recursive=not args.no_recursive).execute_query().value
    print(report.summary())
    print("Report:", write_report(report, args.output))

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
