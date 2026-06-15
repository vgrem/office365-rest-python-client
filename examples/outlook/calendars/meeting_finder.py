"""
Find meeting times and list rooms in the tenant.

Requires delegated permissions Calendars.ReadWrite, MailboxSettings.Read,
Place.Read.All.
"""

from datetime import timedelta

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    attendees = ["meganb@contoso.onmicrosoft.com"]

    result = client.me.find_meeting_times(
        attendees=attendees, meeting_duration=timedelta(hours=1), max_candidates=5
    ).execute_query()

    for s in result.value.meetingTimeSuggestions:
        slot = s.meeting_time_slot
        print(f"  {slot.start} — {slot.end}  (confidence: {s.confidence})")


if __name__ == "__main__":
    main()
