from datetime import datetime, timedelta
from typing import Optional

from office365.outlook.calendar.calendar import Calendar
from office365.outlook.calendar.email_address import EmailAddress

from tests import create_unique_name, test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestCalendar(GraphDelegatedTestCase):
    """Tests for Calendar"""

    cal_name = create_unique_name("Volunteer")
    target_cal: Optional[Calendar] = None

    @requires_delegated(
        "Calendars.Read.Shared",
        "Calendars.ReadWrite.Shared",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test1_find_my_meeting_times(self):
        result = self.client.me.find_meeting_times().execute_query()
        self.assertIsNotNone(result.value.meetingTimeSuggestions)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test2_get_my_schedule(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        result = self.client.me.calendar.get_schedule(
            schedules=[test_user_principal_name],
            start_time=start_time,
            end_time=end_time,
        ).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.ReadWrite",
        "Calendars.Read",
        "Calendars.ReadWrite.Shared",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test3_list_my_cal_groups(self):
        cal_groups = self.client.me.calendar_groups.get().execute_query()
        self.assertIsNotNone(cal_groups.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.ReadWrite",
        "Calendars.Read",
        "Calendars.ReadWrite.Shared",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test4_list_my_cal_permissions(self):
        result = self.client.me.calendar.calendar_permissions.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test5_list_my_cal_view(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        result = self.client.me.get_calendar_view(start_dt=start_time, end_dt=end_time).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.Read",
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test6_get_my_reminder_view(self):
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        result = self.client.me.get_reminder_view(start_dt=start_time, end_dt=end_time).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test7_list_my_events(self):
        result = self.client.me.calendar.events.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test8_list_my_calendars(self):
        result = self.client.me.calendars.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test9_create_cal(self):
        result = self.client.me.calendars.add(name=self.cal_name).execute_query()
        self.assertIsNotNone(result.resource_path)
        TestCalendar.target_cal = result

    @requires_delegated(
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_10_update_cal(self):
        cal = TestCalendar.target_cal
        assert cal is not None
        TestCalendar.cal_name = self.cal_name + "_Updated"
        cal.set_property("name", self.cal_name).update().execute_query()

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_11_get_cal(self):
        cal = TestCalendar.target_cal
        assert cal is not None and cal.id is not None
        result = self.client.me.calendars[cal.id].select(["name", "owner"]).get().execute_query()
        self.assertEqual(result.name, self.cal_name)
        self.assertIsInstance(result.owner, EmailAddress)

    @requires_delegated(
        "Calendars.ReadWrite",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_12_delete_cal(self):
        cal = TestCalendar.target_cal
        assert cal is not None
        cal.delete_object().execute_query()

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        or_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_13_allowed_calendar_sharing_roles(self):
        result = self.client.me.calendar.allowed_calendar_sharing_roles(test_user_principal_name).execute_query()
        self.assertIsNotNone(result.value)
