from __future__ import annotations

from dataclasses import dataclass

from office365.communications.broadcastmeetingaudience import BroadcastMeetingAudience
from office365.runtime.client_value import ClientValue


@dataclass
class BroadcastMeetingSettings(ClientValue):
    """Represents settings related to a live event in Microsoft Teams.

    Fields:
        allowedAudience: ...
        isAttendeeReportEnabled: ...
        isQuestionAndAnswerEnabled: ...
        isRecordingEnabled: ...
        isVideoOnDemandEnabled: ...
    """

    allowedAudience: BroadcastMeetingAudience | None = None
    isAttendeeReportEnabled: bool | None = None
    isQuestionAndAnswerEnabled: bool | None = None
    isRecordingEnabled: bool | None = None
    isVideoOnDemandEnabled: bool | None = None
