"""
Pre-migration assessment — surface blockers and warnings before moving data.

Basic usage of the modular ``MigrationAssessor``: scan the site, then print a
summary plus the flagged issues (blockers block a migration, warnings are
advisory). Optionally export the full report to Excel.

The assessment is the "scan" phase of the SPMT-style workflow — pair it with
``MigrationJob`` (see ``migrate_files.py`` / ``export_list_to_json.py``) to
assess, then migrate, then verify.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import argparse

from office365.migration import MigrationAssessor
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Assess a SharePoint site for migration readiness")
    parser.add_argument("--permissions", action="store_true", help="scan for unique permissions (slower)")
    parser.add_argument("--output", help="optional path to export the report as Excel (.xlsx)")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    assessor = MigrationAssessor(ctx.web)
    if args.permissions:
        assessor.include_permissions()

    report = assessor.assess().execute_query().value
    print(report.summary())

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

    if args.output:
        report.to_excel(args.output)
        print(f"\nReport exported to {args.output}")


if __name__ == "__main__":
    main()
