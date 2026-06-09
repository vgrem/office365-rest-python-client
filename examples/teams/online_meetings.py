"""
Online meetings — create Teams meetings with join links for
scheduling automation.

Creates a Teams meeting accessible via a generated join URL.
Supports meeting settings (lobby, chat, recording), custom
start/end time, and participant configuration.

Useful for:
  - Automated scheduling bots
  - Meeting room booking systems
  - CRM integrations that create Teams meetings

Requires delegated permission ``OnlineMeetings.ReadWrite.All``.

https://learn.microsoft.com/en-us/graph/api/resources/onlinemeeting
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_client_secret, test_tenant


def main():
    client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)

    start = datetime.now(timezone.utc) + timedelta(days=1, hours=9)
    end = start + timedelta(hours=1)

    meeting = client.me.online_meetings.create(
        start_datetime=start, end_datetime=end, subject="Project sync — SDK demo"
    ).execute_query()

    print(f"Meeting: {meeting.subject}")
    print(f"  Join: {meeting.join_web_url}")
    print(f"  Start: {meeting.start_datetime}")
    print(f"  End: {meeting.end_datetime}")

    meeting2 = client.me.online_meetings.create(
        start_datetime=start + timedelta(days=1),
        end_datetime=end + timedelta(days=1),
        subject="All-hands with lobby control",
        lobbyBypassSettings={"scope": "organization", "isDialInBypassEnabled": False},
        allowMeetingChat="enabled",
        allowTranscription=True,
    ).execute_query()

    print(f"\nMeeting: {meeting2.subject}")
    print(f"  Join: {meeting2.join_web_url}")
    print(f"  Chat: {meeting2.allow_meeting_chat}")
    print(f"  Transcript: {meeting2.allow_transcription}")

    fetched = client.me.online_meetings.get_by_join_web_url(meeting2.join_web_url).execute_query()
    print(f"\nFetched by join URL: {fetched.subject}")

    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    recent = client.me.online_meetings.filter(f"startDateTime ge {since}").top(10).get().execute_query()
    print(f"\nRecent meetings: {len(recent)}")
    for m in recent:
        print(f"  {m.start_datetime}  {m.subject}  {m.join_web_url}")


if __name__ == "__main__":
    main()
