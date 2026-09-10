"""
Export messages for compliance/backup using the deferred collection adapters.

    python export_messages.py --output ./messages --team <team-id>
    python export_messages.py --output ./messages --user user@contoso.com
    python export_messages.py --output ./messages --filter "createdDateTime gt 2024-01-01T00:00:00Z"

Writes ``messages.ndjson`` and (unless ``--no-attachments``) inline images under
``attachments/``. Everything is deferred: the single ``execute_query()`` pages
through the results and writes the files.

Requires application permission Teamwork.Migrate.All (plus the matching read
permissions for the chosen scope).
"""

import argparse
from pathlib import Path

from office365.graph_client import GraphClient
from tests.settings import client_id, client_secret, tenant


def main():
    parser = argparse.ArgumentParser(description="Export Teams messages to NDJSON")
    parser.add_argument("--output", default="./messages_export", help="output directory")
    parser.add_argument("--team", default=None, help="team id (all channel messages)")
    parser.add_argument("--user", default=None, help="user id/UPN (that user's chats)")
    parser.add_argument("--filter", default=None, help="OData $filter, e.g. a date range")
    parser.add_argument("--no-attachments", action="store_true", help="skip hosted contents")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_client_secret(client_id, client_secret)

    if args.team:
        messages = client.teams[args.team].channels.get_all_messages()
    elif args.user:
        messages = client.users[args.user].chats.get_all_messages()
    else:
        messages = client.teams.get_all_messages()
    if args.filter:
        messages.filter(args.filter)

    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "messages.ndjson", "w", encoding="utf-8") as f:
        chain = messages.get_all().to_ndjson(f)
        if not args.no_attachments:
            chain.download_hosted_contents(out / "attachments")
        chain.execute_query()

    print(f"Exported {len(messages)} messages to {out / 'messages.ndjson'}")


if __name__ == "__main__":
    main()
