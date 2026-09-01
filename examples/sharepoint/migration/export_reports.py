"""
Migrate a directory tree and write summary/Item/Failure reports.

Demonstrates the "monitor and report" phase of the migration workflow: run a
``MigrationJob``, then export its results as CSV + JSON through the records
interchange. The failure report is only written when failures occur.

Requires: nothing beyond the library.
"""

import argparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget


def main():
    parser = argparse.ArgumentParser(description="Migrate a directory tree and export reports")
    parser.add_argument("--source", required=True, help="source directory")
    parser.add_argument("--target", required=True, help="target directory")
    parser.add_argument("--reports", default="reports", help="output directory for the reports")
    args = parser.parse_args()

    job = MigrationJob(FileSystemSource(args.source), FileSystemTarget(args.target))
    job.plan()
    stats = job.run()
    print(stats.summary())
    print(job.verify().summary())

    written = job.export_reports(args.reports)
    print("\nReports:", ", ".join(written))


if __name__ == "__main__":
    main()
