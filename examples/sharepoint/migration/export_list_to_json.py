"""
Export a SharePoint list to local JSON records — migrate "from SharePoint".

The ``SharePointListSource`` adapter projects the list items into record
payloads (the canonical data-pipeline form) and ``JsonFileTarget`` persists each
record as one JSON file under a local directory. Reverse the direction with the
``SharePointListTarget`` adapter to import records back into a list.

Requires: read access to the source list.
"""

import argparse

from office365.migration import MigrationJob
from office365.migration.adapters.filesystem import JsonFileTarget
from office365.migration.adapters.sharepoint import SharePointListSource
from office365.sharepoint.client_context import ClientContext
from tests.settings import client_id, password, team_site_url, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Export a SharePoint list to local JSON records")
    parser.add_argument("--list-title", required=True, help="source list title")
    parser.add_argument("--target", default="/tmp", help="directory to write the JSON records into")
    parser.add_argument("--select", default=None, help="comma-separated fields to export")
    args = parser.parse_args()

    ctx = ClientContext(team_site_url).with_username_and_password(
        tenant=tenant, client_id=client_id, username=username, password=password
    )
    source = SharePointListSource(
        ctx.web.lists.get_by_title(args.list_title),
        select=args.select.split(",") if args.select else None,
    )

    job = MigrationJob(source, JsonFileTarget(args.target))
    manifest = job.plan()
    print(f"Planned {len(manifest)} list items")

    stats = job.run()
    print(stats.summary())

    report = job.verify()
    print(report.summary())


if __name__ == "__main__":
    main()
