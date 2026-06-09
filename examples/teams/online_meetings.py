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

    # -- Step 1: create a Teams meeting --
    start = datetime.now(timezone.utc) + timedelta(days=1, hours=9)
    end = start + timedelta(hours=1)

    meeting = client.me.online_meetings.create(
        startDateTime=start.isoformat(),
        endDateTime=end.isoformat(),
        subject="Project sync — SDK demo",
        description="Weekly sync with demo team.",
    ).execute_query()

    print("Meeting created:\n")
    print(f"  Subject:     {meeting.subject}")
    print(f"  Join link:   {meeting.join_web_url}")
    print(f"  Start:       {meeting.start_date_time.strftime('%Y-%m-%d %H:%M') if meeting.start_date_time else '?'}")
    print(f"  End:         {meeting.end_date_time.strftime('%Y-%m-%d %H:%M') if meeting.end_date_time else '?'}")

    # -- Step 2: create with lobby and chat settings --
    meeting2 = client.me.online_meetings.create(
        startDateTime=(start + timedelta(days=1)).isoformat(),
        endDateTime=(end + timedelta(days=1)).isoformat(),
        subject="All-hands with lobby control",
        description="Lobby bypass disabled for external participants.",
        lobbyBypassSettings={
            "scope": "organization",
            "isDialInBypassEnabled": False,
        },
        allowMeetingChat="enabled",
        allowTranscription=True,
    ).execute_query()

    print("\nMeeting with lobby control:\n")
    print(f"  Subject:     {meeting2.subject}")
    print(f"  Join link:   {meeting2.join_web_url}")
    print(f"  Chat:        {meeting2.allow_meeting_chat}")
    print(f"  Transcript:  {meeting2.allow_transcription}")

    # -- Step 3: get meeting details by join web URL --
    fetched = client.me.online_meetings.get_by_join_web_url(meeting2.join_web_url).execute_query()
    print(f"\nFetched by join URL: {fetched.subject}")

    # -- Step 4: list recent meetings (last 30 days) --
    since = (datetime.now(timezone.utc) - timedelta(days=30)).isoformat()
    recent = client.me.online_meetings.filter(f"startDateTime ge {since}").top(10).get().execute_query()
    print(f"\nRecent meetings: {len(recent)}")
    for m in recent:
        start_str = m.start_date_time.strftime("%m-%d") if m.start_date_time else "?"
        print(f"  {start_str}  {m.subject[:45]:45s}  {m.join_web_url}")


if __name__ == "__main__":
    main()
