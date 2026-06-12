"""
Create Teams online meetings with join links.

Requires delegated permission OnlineMeetings.ReadWrite.All.
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    start = datetime.now(timezone.utc) + timedelta(days=1, hours=9)
    end = start + timedelta(hours=1)

    meeting = client.me.online_meetings.create(
        start_datetime=start, end_datetime=end, subject="Project sync — SDK demo"
    ).execute_query()

    meeting2 = client.me.online_meetings.create(
        start_datetime=start + timedelta(days=1),
        end_datetime=end + timedelta(days=1),
        subject="All-hands with lobby control",
        lobbyBypassSettings={"scope": "organization", "isDialInBypassEnabled": False},
        allowMeetingChat="enabled",
        allowTranscription=True,
    ).execute_query()

    print(f"Created: {meeting.subject}  {meeting.join_web_url}")
    print(f"Created: {meeting2.subject}  {meeting2.join_web_url}  chat={meeting2.allow_meeting_chat}")


if __name__ == "__main__":
    main()
