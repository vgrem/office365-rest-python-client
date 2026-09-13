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

from office365.migration import AssessmentOptions, MigrationAssessor, MigrationTenantAssessor
from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests.settings import admin_site_url, client_id, password, tenant, username


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
    parser.add_argument("--size-threshold", type=float, default=500.0, help="size guidance in GB")
    parser.add_argument("--output", default="/tmp", help="directory for the LargeSites-detail report")
    args = parser.parse_args()

    if args.site_url:
        ctx = ClientContext(args.site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        options = AssessmentOptions(
            disabled_scans={"permissions", "fields", "paths", "files"},
            large_site_threshold_gb=args.size_threshold,
        )
        print("Assessing site…", flush=True)
        report = MigrationAssessor(ctx.web, options).assess().execute_query().value
    else:
        ctx = ClientContext(admin_site_url).with_username_and_password(
            tenant=tenant, client_id=client_id, username=username, password=password
        )
        options = AssessmentOptions(large_site_threshold_gb=args.size_threshold)
        print("Scanning tenant…", flush=True)
        report = MigrationTenantAssessor(Tenant(ctx), options).assess().execute_query().value
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
