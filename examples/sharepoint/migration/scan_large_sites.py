"""
Generate the SMAT-style ``LargeSites-detail`` scan report — site collections
over a size threshold across the tenant.

Enumerates site collections at **tenant scope** via the SPO.Tenant admin API
(the SMAT model: get the site list first, then report the large ones) and
writes only the sites above the size guidance (``--size-threshold``, default
500 GB) as one JSON file. Mirrors the SharePoint Migration Assessment Tool's
``LargeSites-detail`` scan:

    python scan_large_sites.py --size-threshold 250

Requires: SharePoint admin access (SPO.Tenant read) — SMAT's farm-account
prerequisite. Use ``--site-url`` for a single-site deep scan instead.
"""

from __future__ import annotations

import argparse
import os

from office365.migration import MigrationAssessor, MigrationTenantAssessor
from office365.migration.assessment.scanners import AssessmentOptions
from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress) -> None:
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)

    return hook


def write_report(output_dir: str, scan) -> str | None:
    """Write the scan's typed rows as one ``LargeSites-detail.json``."""
    if scan is None or not scan.records:
        return None
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "LargeSites-detail.json")
    with open(path, "w", encoding="utf-8") as f:
        f.write(scan.to_json())
    return path


def main():
    parser = argparse.ArgumentParser(description="Write the SMAT LargeSites-detail scan report")
    parser.add_argument("--site-url", help="single site collection deep scan (skips tenant scope)")
    parser.add_argument("--size-threshold", type=float, default=1.0, help="size guidance in GB (default: 500)")
    parser.add_argument("--output", default="/tmp", help="directory for the LargeSites-detail report")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    if args.site_url:
        ctx = ClientContext(args.site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        options = AssessmentOptions(
            disabled_scans={"permissions", "fields", "paths", "files"},
            large_site_threshold_gb=args.size_threshold,
        )
        hook = None if args.no_progress else progress_bar("Assessing")
        report = MigrationAssessor(ctx.web, options).assess(progress=hook).execute_query().value
    else:
        ctx = ClientContext(admin_site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        options = AssessmentOptions(large_site_threshold_gb=args.size_threshold)
        hook = None if args.no_progress else progress_bar("Scanning tenant")
        report = MigrationTenantAssessor(Tenant(ctx), options).assess(progress=hook).execute_query().value
    print(report.summary())

    scan = report.scan_reports.get("LargeSites")
    path = write_report(args.output, scan)
    if path is not None and scan is not None:
        print(f"\n{len(scan.records)} site(s) over the {args.size_threshold:g} GB size guidance:")
        print("Report:", path)
    else:
        print(f"\nNo site collections over the {args.size_threshold:g} GB size guidance were found.")


if __name__ == "__main__":
    main()
