"""
Generate the SMAT-style ``LargeSites-detail.csv`` scan report — the list of all
site collections over 500 GB.

Runs the ``LargeSites`` scan against one or more site collections and writes
only the sites that exceed the SPMT size guidance (500 GB), using the SMAT
report columns. Mirrors the SharePoint Migration Assessment Tool's output:

    python scan_large_sites.py --site-url https://contoso.sharepoint.com/sites/big --output out/
    python scan_large_sites.py --sites-file sites.txt --output out/

Requires: read access to each site collection.
"""

from __future__ import annotations

import argparse
import csv
import json
import os

from office365.migration import MigrationAssessor
from office365.migration.assessment.scanners import AssessmentOptions
from office365.runtime.operations import Progress
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username

# The LargeSites report only needs site-level data — list-level issue scans
# (fields/paths/files/permissions) are skipped to keep the scan cheap.
_OPTIONS = AssessmentOptions(disabled_scans={"permissions", "fields", "paths", "files"})


def progress_bar(description: str):
    """tqdm-backed hook — the library only needs a ``Callable[[Progress], None]``."""
    from tqdm import tqdm

    bar = tqdm(desc=description)

    def hook(p: Progress) -> None:
        if p.total is not None and bar.total is None:
            bar.total = p.total
        bar.update(p.done - bar.n)

    return hook


def collect_large_sites(urls: list[str], no_progress: bool = False) -> tuple[list[str], list[dict]]:
    """Scan each site collection and return (columns, rows) for the report."""
    columns: list[str] = []
    rows: list[dict] = []
    for url in urls:
        ctx = ClientContext(url).with_username_and_password(tenant, client_id, username, password)
        hook = None if no_progress else progress_bar(f"Assessing {url}")
        report = MigrationAssessor(ctx.web, _OPTIONS).assess(progress=hook).execute_query().value
        print(report.summary())

        scan = report.scan_reports.get("LargeSites")
        if scan is None:
            continue
        if not columns:
            columns = list(scan.columns)
        rows.extend(r for r in scan.records if isinstance(r.get("SizeInGB"), (int, float)))
    return columns, rows


def write_large_sites_report(output_dir: str, columns: list[str], rows: list[dict]) -> list[str]:
    """Write ``LargeSites-detail.csv`` + ``.json`` (SMAT layout), largest first."""
    if not rows:
        return []
    os.makedirs(output_dir, exist_ok=True)
    rows = sorted(rows, key=lambda r: r.get("SizeInGB") or 0, reverse=True)

    csv_path = os.path.join(output_dir, "LargeSites-detail.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns, restval="n/a")
        writer.writeheader()
        writer.writerows(rows)

    json_path = os.path.join(output_dir, "LargeSites-detail.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)

    return [csv_path, json_path]


def main():
    parser = argparse.ArgumentParser(description="Write the SMAT LargeSites-detail.csv scan report")
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--site-url", default=team_site_url, help="site collection URL to scan")
    group.add_argument("--sites-file", help="file with one site collection URL per line")
    parser.add_argument("--output", default="reports", help="directory for the LargeSites-detail report")
    parser.add_argument("--no-progress", action="store_true", help="do not show tqdm progress bars")
    args = parser.parse_args()

    urls = [args.site_url]
    if args.sites_file:
        urls = [line.strip() for line in open(args.sites_file, encoding="utf-8") if line.strip()]

    columns, rows = collect_large_sites(urls, no_progress=args.no_progress)
    written = write_large_sites_report(args.output, columns, rows)
    if written:
        print(f"\n{len(rows)} site(s) over the SPMT size guidance:")
        print("Report:", ", ".join(written))
    else:
        print("\nNo site collections over the SPMT size guidance were found.")


if __name__ == "__main__":
    main()
