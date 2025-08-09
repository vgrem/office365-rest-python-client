from office365.communications.types import BroadcastMeetingAudience
from office365.runtime.client_value import ClientValue


class BroadcastMeetingSettings(ClientValue):
    """Represents settings related to a live event in Microsoft Teams."""

    def __init__(
        self,
        allowed_audience: BroadcastMeetingAudience = None,
        is_attendee_report_enabled: bool = None,
        is_question_and_answer_enabled: bool = None,
        is_recording_enabled: bool = None,
        is_video_on_demand_enabled: bool = None,
    ):
        self.allowedAudience = allowed_audience
        self.isAttendeeReportEnabled = is_attendee_report_enabled
        self.isQuestionAndAnswerEnabled = is_question_and_answer_enabled
        self.isRecordingEnabled = is_recording_enabled
        self.isVideoOnDemandEnabled = is_video_on_demand_enabled
