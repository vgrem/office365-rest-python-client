"""
Assess multiple sites in bulk — a tenant-wide readiness review.

Reads a file with one site URL per line, runs the recursive assessment for each
site, and aggregates the results into a combined report. Useful for tenant-level
readiness reviews before a migration program. Per-scan detail records (e.g. the
LargeSites list) are merged so the combined report holds one row per site.

Requires: read access to each site.
"""

import argparse

from office365.migration import MigrationAssessor
from office365.migration.assessment.report import AssessmentReport, ScanReport
from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, tenant, username


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
    parser = argparse.ArgumentParser(description="Bulk-assess a list of sites")
    parser.add_argument("--sites-file", required=True, help="file with one site URL per line")
    parser.add_argument("--no-progress", action="store_true", help="do not show tqdm progress bars")
    args = parser.parse_args()

    urls = [line.strip() for line in open(args.sites_file, encoding="utf-8") if line.strip()]
    combined = AssessmentReport()

    for url in urls:
        ctx = ClientContext(url).with_username_and_password(tenant, client_id, username, password)
        hook = None if args.no_progress else progress_bar(f"Assessing {url}")
        report = MigrationAssessor(ctx.web).assess(progress=hook).execute_query().value
        print(report.summary())

        combined.total_webs += report.total_webs
        combined.total_lists += report.total_lists
        combined.total_files += report.total_files
        combined.total_size_gb += report.total_size_gb
        combined.lists_skipped = combined.lists_skipped or report.lists_skipped
        combined.webs_skipped = combined.webs_skipped or report.webs_skipped
        combined.issues.extend(report.issues)
        _merge_scan_reports(combined, report)

    print(f"\nCombined ({len(urls)} sites):")
    print(combined.summary())


def _merge_scan_reports(combined: AssessmentReport, report: AssessmentReport) -> None:
    """Concatenate per-scan detail records across sites (one row per site)."""
    for name, scan in report.scan_reports.items():
        if name in combined.scan_reports:
            combined.scan_reports[name].records.extend(scan.records)
        else:
            combined.scan_reports[name] = ScanReport(name, scan.container, scan.columns, list(scan.records))


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()
