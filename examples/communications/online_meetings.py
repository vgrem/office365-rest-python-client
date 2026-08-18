"""
Create a Teams online meeting and list your upcoming meetings.

Requires delegated permission ``OnlineMeetings.ReadWrite``.

https://learn.microsoft.com/en-us/graph/api/application-post-onlinemeetings
"""

import argparse
from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, username


def main():
    parser = argparse.ArgumentParser(description="Create a Teams meeting")
    parser.add_argument("--subject", default="Project sync", help="Meeting subject")
    parser.add_argument("--minutes", type=int, default=60, help="Meeting duration in minutes")
    args = parser.parse_args()

    client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)
    start = datetime.now(timezone.utc) + timedelta(hours=1)
    end = start + timedelta(minutes=args.minutes)

    meeting = client.me.online_meetings.add(
        subject=args.subject,
        startDateTime=start.isoformat(),
        endDateTime=end.isoformat(),
    ).execute_query()
    print(f"Meeting created: {meeting.subject}")
    print(f"  Join URL: {meeting.join_web_url}")

    meetings = client.me.online_meetings.get().execute_query()
    print(f"\nYour upcoming meetings ({len(meetings)}):")
    for m in meetings:
        props = m.properties
        print(f"  {props.get('subject', '(no subject)'):40s}  {props.get('startDateTime', '?')}")


if __name__ == "__main__":
    main()
