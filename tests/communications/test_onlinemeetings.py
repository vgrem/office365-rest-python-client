from datetime import datetime, timedelta

import pytz

from office365.communications.onlinemeetings.online_meeting import OnlineMeeting
from tests.graph_case import GraphTestCase


class TestOnlineMeetings(GraphTestCase):
    target_meeting = None  # type: OnlineMeeting

    @classmethod
    def setUpClass(cls):
        super(TestOnlineMeetings, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        pass

    def test1_create_meeting(self):
        result = self.client.me.online_meetings.create(
            subject="User Token Meeting"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_meeting = result

    def test2_get_meeting(self):
        meeting_id = self.__class__.target_meeting.id
        result = self.client.me.online_meetings[meeting_id].get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test3_get_virtual_appointment_join_web_url(self):
    #    result = (
    #        self.__class__.target_meeting.get_virtual_appointment_join_web_url().execute_query()
    #    )
    #    self.assertIsNotNone(result.value)

    def test4_update_meeting(self):
        now = datetime.now(pytz.utc)
        update_meeting = self.__class__.target_meeting
        update_meeting.subject = "Patch Meeting Subject"
        update_meeting.start_datetime = now
        update_meeting.end_datetime = now + timedelta(hours=1)
        update_meeting.update().execute_query()

    def test5_delete_meeting(self):
        self.__class__.target_meeting.delete_object().execute_query()
