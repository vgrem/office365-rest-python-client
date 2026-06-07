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
from tests import (
    test_client_id,
    test_password,
    test_tenant,
    test_user_principal_name,
    test_username,
)

client = GraphClient(tenant=test_tenant).with_username_and_password(test_client_id, test_username, test_password)

# 1. Find suggested meeting times
suggestions = client.me.find_meeting_times().execute_query()
for s in suggestions.meeting_time_suggestions or []:
    times = s.meeting_time_slot
    print(f"  Suggested: {times.start.date_time} — {times.end.date_time}")

# 2. Get free/busy schedule for a user
end_time = datetime.now()
start_time = end_time - timedelta(days=7)
schedule = client.me.calendar.get_schedule(
    schedules=[test_user_principal_name],
    start_time=start_time,
    end_time=end_time,
).execute_query()
for item in schedule.value or []:
    print(f"\n  Schedule for: {item.schedule_id}")
    for slot in item.availability_view or []:
        print(f"    {slot.status}: {slot.start.date_time} — {slot.end.date_time}")
