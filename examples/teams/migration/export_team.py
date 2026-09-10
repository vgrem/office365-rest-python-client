"""
Export Teams to a resumable archive via the unified MigrationJob.

    python export_team.py --team <id> --output ./backup --files
    python export_team.py --all --output ./backup

Archive layout: ``<team-id>/team.json``, ``messages.ndjson``, ``attachments/``
and ``files/<channel>.zip`` (with ``--files``). Re-running resumes from the
checkpoint.

Requires application permissions: Team.ReadBasic.All, TeamMember.Read.All,
ChannelMessage.Read.All, Chat.Read.All (and Files.Read.All with --files).
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from office365.migration import MigrationJob
from office365.migration.teams import TeamsArchiveSource, TeamsArchiveTarget, TeamsExportOptions
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Export Teams to a resumable archive")
    parser.add_argument("--team", action="append", default=[], help="team id (repeatable)")
    parser.add_argument("--all", action="store_true", help="export every team in the tenant")
    parser.add_argument("--output", default="./teams_export", help="output directory")
    parser.add_argument("--files", action="store_true", help="also download channel files")
    parser.add_argument("--no-messages", action="store_true", help="skip messages")
    parser.add_argument("--resume", action="store_true", help="continue from the checkpoint")
    args = parser.parse_args()

    if not args.team and not args.all:
        parser.error("pass --team <id> (repeatable) or --all")

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)
    options = TeamsExportOptions(include_files=args.files, include_messages=not args.no_messages)

    source = TeamsArchiveSource(client, team_ids=args.team or None, options=options)
    target = TeamsArchiveTarget(args.output)
    checkpoint = Path(args.output).with_name(Path(args.output).name + ".checkpoint.json")
    job = MigrationJob(source, target, checkpoint_path=checkpoint)

    if args.resume:
        stats = job.resume()
    else:
        job.plan()
        stats = job.run()
    print(stats.summary())
    print(job.verify().summary())
    print(f"Archive: {args.output}")


if __name__ == "__main__":
    main()
