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

    room_lists = client.places.room_lists.get().execute_query()
    if room_lists:
        for rl in room_lists:
            print(f"Room list: {rl.display_name}  ({rl.email_address or ''})")
            try:
                rooms = rl.rooms.get().execute_query()
                for room in rooms:
                    print(f"  {room.display_name}  {room.email_address}  (capacity: {room.capacity})")
            except Exception:
                pass

    attendees = ["meganb@contoso.onmicrosoft.com"]
    if room_lists:
        try:
            rooms = room_lists[0].rooms.get().execute_query()
            attendees.extend(r.email_address for r in rooms[:2] if r.email_address)
        except Exception:
            pass

    result = client.me.find_meeting_times(
        attendees=attendees, meeting_duration=timedelta(hours=1), max_candidates=5
    ).execute_query()
    if result and result.value and result.value.meeting_time_suggestions:
        for s in result.value.meeting_time_suggestions:
            slot = s.meeting_time_slot
            print(f"  {slot.start} — {slot.end}  (confidence: {s.confidence})")


if __name__ == "__main__":
    main()
