from datetime import datetime, timedelta
from typing import Optional

import pytz
from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestOnlineMeetings(GraphDelegatedTestCase):
    target_meeting: Optional[OnlineMeeting] = None

    @requires_delegated("OnlineMeetings.ReadWrite", bypass_roles=["Teams Administrator", "Global Administrator"])
    def test1_create_meeting(self):
        """Creates an online meeting"""
        result = self.client.me.online_meetings.create(subject="User Token Meeting").execute_query()
        self.assertIsNotNone(result.resource_path)
        TestOnlineMeetings.target_meeting = result

    @requires_delegated("OnlineMeetings.ReadWrite", bypass_roles=["Teams Administrator", "Global Administrator"])
    def test2_get_meeting(self):
        """Gets an online meeting by ID"""
        assert TestOnlineMeetings.target_meeting is not None, "Meeting must be created"
        meeting_id = TestOnlineMeetings.target_meeting.id
        assert meeting_id is not None, "Meeting ID must not be None"
        result = self.client.me.online_meetings[meeting_id].get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test3_get_virtual_appointment_join_web_url(self):
    #    result = (
    #        TestOnlineMeetings.target_meeting.get_virtual_appointment_join_web_url().execute_query()
    #    )
    #    self.assertIsNotNone(result.value)

    @requires_delegated("OnlineMeetings.ReadWrite", bypass_roles=["Teams Administrator", "Global Administrator"])
    def test4_update_meeting(self):
        """Updates an online meeting"""
        assert TestOnlineMeetings.target_meeting is not None, "Meeting must be created"
        now = datetime.now(pytz.utc)
        update_meeting = TestOnlineMeetings.target_meeting
        update_meeting.subject = "Patch Meeting Subject"
        update_meeting.start_datetime = now
        update_meeting.end_datetime = now + timedelta(hours=1)
        update_meeting.update().execute_query()

    @requires_delegated("OnlineMeetings.ReadWrite", bypass_roles=["Teams Administrator", "Global Administrator"])
    def test5_delete_meeting(self):
        """Deletes an online meeting"""
        assert TestOnlineMeetings.target_meeting is not None, "Meeting must be created"
        TestOnlineMeetings.target_meeting.delete_object().execute_query()
