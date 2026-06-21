"""
Find meeting times and get free/busy schedules for users.

Two complementary patterns: find suggested meeting slots based on
availability, then get the full schedule for a user.

Requires delegated permission ``Calendars.ReadWrite`` and
``User.Read.All``.

https://learn.microsoft.com/en-us/graph/api/user-findmeetingtimes
https://learn.microsoft.com/en-us/graph/api/calendar-getschedule
"""

from datetime import datetime, timedelta

from office365.graph_client import GraphClient
from tests.settings import client_id, password, tenant, user_principal, username

client = GraphClient(tenant=tenant).with_username_and_password(client_id, username, password)

# 1. Find suggested meeting times
result = client.me.find_meeting_times().execute_query()
for s in result.value.meetingTimeSuggestions:
    print(f"  Suggested: {s.meetingTimeSlot.start} — {s.meetingTimeSlot.end}")

# 2. Get free/busy schedule for a user
end_time = datetime.now()
start_time = end_time - timedelta(days=7)
schedule = client.me.calendar.get_schedule(
    schedules=[user_principal],
    start_time=start_time,
    end_time=end_time,
).execute_query()
for item in schedule.value:
    print(f"\n  Schedule for: {item.scheduleId}")
    for slot in item.scheduleItems:
        print(f"    {slot.status}: {slot.start} — {slot.end}")
