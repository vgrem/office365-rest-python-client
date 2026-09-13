"""
Monitor a local migration job — pause and resume.

Mirrors SPMT's pause/resume: press Ctrl-C once to pause at the next item
boundary (state is saved to a checkpoint), then run the same command again to
resume from where it stopped:

    python monitor.py --source ./data --target ./dst
    # pause with Ctrl-C, then re-run the same command to resume

Requires: nothing beyond the library.
"""

import argparse
import os
import tempfile

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import FileSystemSource, FileSystemTarget


def main():
    parser = argparse.ArgumentParser(description="Run a migration under a live monitor (Ctrl-C to pause)")
    parser.add_argument("--source", required=True, help="source directory")
    parser.add_argument("--target", required=True, help="target directory")
    args = parser.parse_args()

    checkpoint = os.path.join(tempfile.gettempdir(), "migration-monitor-checkpoint.json")
    manifest = os.path.join(tempfile.gettempdir(), "migration-monitor-manifest.json")

    job = MigrationJob(
        FileSystemSource(args.source),
        FileSystemTarget(args.target),
        manifest_path=manifest,
        checkpoint_path=checkpoint,
    )
    print("Planning…", flush=True)
    plan = job.plan()
    print(f"Planned {len(plan)} files -> {args.target}")

    try:
        print("Migrating… (Ctrl-C to pause)", flush=True)
        stats = job.run()
        print(stats.summary())
        print(job.verify().summary())
    except KeyboardInterrupt:
        job.pause()
        print("\nPaused at the next item boundary — re-run the same command to resume.")


if __name__ == "__main__":
    main()
