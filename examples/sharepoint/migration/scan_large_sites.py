"""
Generate the SMAT-style ``LargeSites-detail.csv`` scan report — the list of all
site collections over 500 GB across the tenant.

Enumerates site collections at **tenant scope** via the SPO.Tenant admin API
(the SMAT model: get the site list first, then report the large ones) and
writes only the sites that exceed the SPMT size guidance. Mirrors the
SharePoint Migration Assessment Tool's ``LargeSites-detail`` scan output:

    python scan_large_sites.py --output out/

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


def write_report(output_dir: str, scan) -> list[str]:
    """Write ``LargeSites-detail.csv`` + ``.json`` from the scan's typed rows."""
    if not scan.records:
        return []
    os.makedirs(output_dir, exist_ok=True)
    csv_path = os.path.join(output_dir, "LargeSites-detail.csv")
    json_path = os.path.join(output_dir, "LargeSites-detail.json")
    with open(csv_path, "w", encoding="utf-8") as f:
        f.write(scan.to_csv())
    with open(json_path, "w", encoding="utf-8") as f:
        f.write(scan.to_json())
    return [csv_path, json_path]


def main():
    parser = argparse.ArgumentParser(description="Write the SMAT LargeSites-detail.csv scan report")
    parser.add_argument("--site-url", help="single site collection deep scan (skips tenant scope)")
    parser.add_argument("--output", default="reports", help="directory for the LargeSites-detail report")
    parser.add_argument("--no-progress", action="store_true", help="do not show a tqdm progress bar")
    args = parser.parse_args()

    if args.site_url:
        ctx = ClientContext(args.site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        options = AssessmentOptions(disabled_scans={"permissions", "fields", "paths", "files"})
        hook = None if args.no_progress else progress_bar("Assessing")
        report = MigrationAssessor(ctx.web, options).assess(progress=hook).execute_query().value
    else:
        ctx = ClientContext(admin_site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        hook = None if args.no_progress else progress_bar("Scanning tenant")
        report = MigrationTenantAssessor(Tenant(ctx)).assess(progress=hook).execute_query().value
    print(report.summary())

    scan = report.scan_reports.get("LargeSites")
    written = write_report(args.output, scan)
    if written and scan is not None:
        print(f"\n{len(scan.records)} site(s) over the SPMT size guidance:")
        print("Report:", ", ".join(written))
    else:
        print("\nNo site collections over the SPMT size guidance were found.")


if __name__ == "__main__":
    main()
