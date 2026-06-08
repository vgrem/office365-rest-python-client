"""Calendar — calendars, meeting times, schedule, permissions, sharing.

Tests cover:
  - Finding meeting times and reading suggestions
  - Getting user schedule for a time range
  - Listing calendar groups and calendar permissions
  - Calendar view and reminder view over date ranges
  - Listing events in a calendar
  - CRUD: creating, updating, getting, and deleting a calendar
  - Allowed calendar sharing roles query
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import ClassVar, Optional

from office365.outlook.calendar.calendar import Calendar
from office365.outlook.calendar.role_type import CalendarRoleType

from tests import create_unique_name, test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase

_CAL_NAME = create_unique_name("SDK_Test_Calendar")


class TestCalendar(GraphDelegatedTestCase):
    """Calendar operations — list, create, update, delete."""

    target_cal: ClassVar[Optional[Calendar]] = None

    @requires_delegated(
        "Calendars.Read.Shared",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_find_meeting_times(self):
        """Finding meeting times returns suggestions."""
        result = self.client.me.find_meeting_times().execute_query()
        self.assertIsNotNone(result.value)
        self.assertIsNotNone(result.value.meetingTimeSuggestions)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_get_schedule(self):
        """Getting user schedule for a 7-day window returns schedule items."""
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
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_list_calendar_groups(self):
        """Listing calendar groups returns a valid collection."""
        groups = self.client.me.calendar_groups.get().execute_query()
        self.assertIsNotNone(groups.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_list_calendar_permissions(self):
        """Listing calendar permissions returns a valid collection."""
        result = self.client.me.calendar.calendar_permissions.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_get_calendar_view(self):
        """Getting the calendar view for a 14-day range returns events."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        result = self.client.me.get_calendar_view(start_dt=start_time, end_dt=end_time).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_06_get_reminder_view(self):
        """Getting reminder view for a 14-day range returns reminders."""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=14)
        result = self.client.me.get_reminder_view(start_dt=start_time, end_dt=end_time).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_07_list_my_calendars(self):
        """Listing all calendars for the user returns a valid collection."""
        result = self.client.me.calendars.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_08_list_my_events(self):
        """Listing events in the default calendar returns a valid collection."""
        result = self.client.me.calendar.events.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_09_create_calendar(self):
        """Creating a new calendar with a unique name should succeed."""
        result = self.client.me.calendars.add(name=_CAL_NAME).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("name"), _CAL_NAME)
        TestCalendar.target_cal = result

    @requires_delegated(
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_10_update_calendar_name(self):
        """Updating a calendar's name should persist."""
        cal = TestCalendar.target_cal
        if not cal:
            self.skipTest("No calendar created from previous test")

        updated_name = f"{_CAL_NAME}_Updated"
        cal.set_property("name", updated_name).update().execute_query()
        TestCalendar.cal_name = updated_name

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_11_get_calendar_by_id(self):
        """Getting a calendar by ID returns the correct calendar."""
        cal = TestCalendar.target_cal
        if not cal or not cal.id:
            self.skipTest("No calendar created from previous test")

        result = self.client.me.calendars[cal.id].select(["name", "owner"]).get().execute_query()
        self.assertEqual(result.get_property("name"), TestCalendar.cal_name)
        self.assertIsNotNone(result.get_property("owner"))

    @requires_delegated(
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_12_delete_calendar(self):
        """Deleting a calendar should succeed."""
        cal = TestCalendar.target_cal
        if not cal:
            self.skipTest("No calendar created from previous test")

        cal.delete_object().execute_query()
        TestCalendar.target_cal = None

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_13_allowed_calendar_sharing_roles(self):
        """Querying allowed calendar sharing roles for a user returns roles."""
        result = self.client.me.calendar.allowed_calendar_sharing_roles(test_user_principal_name).execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Calendars.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_14_share_calendar_with_user(self):
        """Sharing the default calendar with another user should succeed."""
        perm = self.client.me.calendar.calendar_permissions.add(
            "samanthab@contoso.onmicrosoft.com", CalendarRoleType.read
        ).execute_query()
        self.assertIsNotNone(perm.id)
        self.assertIsNotNone(perm.role)

    @classmethod
    def tearDownClass(cls):
        cal = cls.target_cal
        if cal and cal.resource_path:
            try:
                cal.delete_object().execute_query()
            except Exception:
                pass
