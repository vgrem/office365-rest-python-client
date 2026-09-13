"""
Migrate a local directory tree into another local directory — the foundational
migration job (filesystem -> filesystem).

Basic usage of the migration toolkit: ``plan`` (enumerate the source), ``run``
(copy files, optionally resume from a persisted checkpoint), and ``verify``
(counts + checksum spot-checks). Passing ``--manifest`` / ``--checkpoint``
persists state so an interrupted run can ``resume`` later (re-drives only the
items that weren't completed).

Requires: nothing beyond the library.
"""

import argparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget


def main():
    parser = argparse.ArgumentParser(description="Copy a directory tree via the migration toolkit")
    parser.add_argument("--source", required=True, help="source directory")
    parser.add_argument("--target", required=True, help="target directory")
    parser.add_argument("--manifest", help="manifest JSON path (persists the plan)")
    parser.add_argument("--checkpoint", help="checkpoint JSON path (enables resume)")
    args = parser.parse_args()

    job = MigrationJob(
        FileSystemSource(args.source),
        FileSystemTarget(args.target),
        manifest_path=args.manifest,
        checkpoint_path=args.checkpoint,
    )

    print("Planning…", flush=True)
    manifest = job.plan()
    print(f"Planned {len(manifest)} files")

    print("Migrating…", flush=True)
    stats = job.run()
    print(stats.summary())

    report = job.verify()
    print(report.summary())


if __name__ == "__main__":
    main()
