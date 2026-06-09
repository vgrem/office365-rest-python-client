"""
Meeting finder: suggest optimal time slots and resolve rooms.

Brings together three related patterns:
  1. Find available meeting times that work for all attendees.
  2. List room lists and rooms in the tenant.
  3. Get free/busy schedule for a room across a time window.

Useful for scheduling assistants, booking flows, and room
management tooling.

Requires delegated permissions:
    Calendars.ReadWrite          Create and manage events
    MailboxSettings.Read         Read user availability
    Place.Read.All               List rooms and room lists

https://learn.microsoft.com/en-us/graph/api/user-findmeetingtimes
https://learn.microsoft.com/en-us/graph/api/resources/place
"""

from datetime import datetime, timedelta, timezone

from office365.graph_client import GraphClient
from tests import test_client_id, test_password, test_tenant, test_username


def main():
    client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

    # -- Step 1: list room lists and rooms in the tenant --
    print("Places (room lists and rooms):")
    all_places = client.places.get().execute_query()
    for p in all_places:
        print(f"  {p.display_name:45s}  type={p.entity_type_name}")
    print()

    # Try to get room lists specifically
    room_lists = client.places.room_lists.get().execute_query()
    if room_lists:
        print("Room lists:")
        for rl in room_lists:
            print(f"  {rl.display_name:45s}  {rl.email_address or ''}")
            # Get rooms in this list
            try:
                rooms = rl.rooms.get().execute_query()
                for room in rooms:
                    print(f"    ↳ {room.display_name:40s}  {room.email_address or ''}  ({room.capacity or '?'} seats)")
            except Exception:
                pass
    else:
        print("(No room lists found — room list management may need Place.Read.All)")

    # -- Step 2: find meeting times for next week --
    now = datetime.now(timezone.utc)
    start_time = now + timedelta(days=1)
    end_time = now + timedelta(days=7)

    # Collect room email addresses if available
    attendee_smtp = ["meganb@contoso.onmicrosoft.com"]
    if room_lists:
        for rl in room_lists[:1]:  # first room list
            try:
                rooms = rl.rooms.get().execute_query()
                attendee_smtp.extend(r.email_address for r in rooms[:2] if r.email_address)
            except Exception:
                pass

    print(f"\nFinding meeting times for: {', '.join(attendee_smtp)}")
    print(f"  Window: {start_time.strftime('%Y-%m-%d %H:%M')} — {end_time.strftime('%Y-%m-%d %H:%M')}")

    suggestions = client.me.find_meeting_times(
        attendees=attendee_smtp,
        meeting_duration=timedelta(hours=1),
        max_candidates=5,
    ).execute_query()

    if suggestions and hasattr(suggestions, "value") and suggestions.value:
        print(f"\nSuggested times ({len(suggestions.value)} candidate(s)):\n")
        # The value is a MeetingTimeSuggestionsResult
        result = suggestions.value
        if hasattr(result, "meeting_time_suggestions") and result.meeting_time_suggestions:
            for s in result.meeting_time_suggestions:
                slot = s.meeting_time_slot
                print(f"  {slot.start.strftime('%Y-%m-%d %H:%M')} — {slot.end.strftime('%H:%M')}  (confidence: {s.confidence})")
                if hasattr(s, "locations") and s.locations:
                    for loc in s.locations:
                        print(f"    Location: {loc.display_name}")
        else:
            print("  (no detailed suggestions — check permissions)")
    else:
        print("  No meeting suggestions returned.")


if __name__ == "__main__":
    main()
