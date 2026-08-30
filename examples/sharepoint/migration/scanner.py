"""
Pre-migration assessment — surface blockers and warnings before moving data.

Basic usage of the modular ``MigrationAssessor``: scan the site, then print a
summary plus the flagged issues (blockers block a migration, warnings are
advisory). A determinate progress bar tracks the per-list scan.

The assessment is the "scan" phase of the SPMT-style workflow — pair it with
``MigrationJob`` (see ``migrate_files.py`` / ``export_list_to_json.py``) to
assess, then migrate, then verify.

https://learn.microsoft.com/en-us/sharepoint/dev/apis/migration-api-reference
"""

import argparse

from office365.migration import MigrationAssessor
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


def main():
    parser = argparse.ArgumentParser(description="Assess a SharePoint site for migration readiness")
    parser.add_argument("--site-url", default=team_site_url, help="site URL to assess")
    parser.add_argument("--permissions", action="store_true", help="scan for unique permissions (slower)")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    ctx = ClientContext(args.site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    assessor = MigrationAssessor(ctx.web)
    if args.permissions:
        assessor.include_permissions()

    hook = None if args.no_progress else progress_bar("Assessing")
    report = assessor.assess(progress=hook).execute_query().value
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


if __name__ == "__main__":
    main()
