"""
Migrate a directory tree and write one JSON migration report.

Demonstrates the "monitor and report" phase of the migration workflow: run a
``MigrationJob``, then write its summary, item, and failure rows as a single
``MigrationReport.json``. The failure section is empty when the run is clean.

Requires: nothing beyond the library.
"""

import argparse
import json
import os

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.migration.report import build_report


def main():
    parser = argparse.ArgumentParser(description="Migrate a directory tree and write one JSON report")
    parser.add_argument("--source", required=True, help="source directory")
    parser.add_argument("--target", required=True, help="target directory")
    parser.add_argument("--reports", default="/tmp", help="directory for the MigrationReport.json")
    args = parser.parse_args()

    job = MigrationJob(FileSystemSource(args.source), FileSystemTarget(args.target))
    job.plan()
    stats = job.run()
    print(stats.summary())
    print(job.verify().summary())

    report = build_report(job)
    os.makedirs(args.reports, exist_ok=True)
    path = os.path.join(args.reports, "MigrationReport.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump({"summary": report.summary, "items": report.items, "failures": report.failures}, f, indent=2)
    print("\nReport:", path)


if __name__ == "__main__":
    main()
