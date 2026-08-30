"""
Migrate a local directory tree into another local directory — the foundational
migration job (filesystem -> filesystem).

Basic usage of the migration toolkit: ``plan`` (enumerate the source), ``run``
(copy files with progress and an optional persisted checkpoint), and ``verify``
(counts + checksum spot-checks). Passing ``--manifest`` / ``--checkpoint``
persists state so an interrupted run can ``resume`` later (re-drives only the
items that weren't completed).

Requires: ``tqdm`` for the progress bars.
"""

import argparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget
from office365.runtime.operations import Progress


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
    parser = argparse.ArgumentParser(description="Copy a directory tree via the migration toolkit")
    parser.add_argument("--source", required=True, help="source directory")
    parser.add_argument("--target", required=True, help="target directory")
    parser.add_argument("--manifest", help="manifest JSON path (persists the plan)")
    parser.add_argument("--checkpoint", help="checkpoint JSON path (enables resume)")
    parser.add_argument("--no-progress", action="store_true", help="do not show tqdm progress bars")
    args = parser.parse_args()

    job = MigrationJob(
        FileSystemSource(args.source),
        FileSystemTarget(args.target),
        manifest_path=args.manifest,
        checkpoint_path=args.checkpoint,
    )

    hook = None if args.no_progress else progress_bar("Scanning")
    manifest = job.plan(progress=hook)
    print(f"Planned {len(manifest)} files")

    hook = None if args.no_progress else progress_bar("Migrating")
    stats = job.run(progress=hook)
    print(stats.summary())

    report = job.verify()
    print(report.summary())


if __name__ == "__main__":
    main()
