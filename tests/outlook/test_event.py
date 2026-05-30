from datetime import datetime, timedelta
from typing import Optional

from office365.outlook.calendar.events.event import Event

from tests import test_user_principal_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOutlookEvent(GraphDelegatedTestCase):
    target_event: Optional[Event] = None

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test2_create_event(self):
        when = datetime.now() + timedelta(days=1)
        result = self.client.me.calendar.events.add(
            subject="Let's go for lunch",
            body="Does mid month work for you?",
            start=when,
            end=when + timedelta(hours=1),
            attendees=[test_user_principal_name],
        ).execute_query()
        self.assertIsNotNone(result.id)
        TestOutlookEvent.target_event = result

    @requires_delegated(
        "Calendars.ReadBasic",
        "Calendars.Read",
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test3_list_my_events(self):
        result = self.client.me.events.get().execute_query()
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test4_update_event(self):
        assert TestOutlookEvent.target_event is not None
        event = TestOutlookEvent.target_event
        event.subject = "Let's go for lunch (updated)"
        event.update().execute_query()

    # def test5_cancel_event(self):
    #    event = self.__class__.target_event
    #    event.cancel().execute_query()

    @requires_delegated(
        "Calendars.ReadWrite",
        "Calendars.ReadWrite.Shared",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test6_delete_event(self):
        assert TestOutlookEvent.target_event is not None
        event_to_delete = TestOutlookEvent.target_event
        event_to_delete.delete_object().execute_query()
        # verify
        events = self.client.me.events.get().execute_query()
        results = [e for e in events if e.id == event_to_delete.id]
        self.assertEqual(len(results), 0)
