from office365.runtime.client_value import ClientValue


class BroadcastMeetingSettings(ClientValue):
    """Represents settings related to a live event in Microsoft Teams."""

    def __init__(self, is_attendee_report_enabled: bool = None):
        self.isAttendeeReportEnabled = is_attendee_report_enabled
