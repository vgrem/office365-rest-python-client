from __future__ import annotations

from datetime import datetime

from office365.common.meeting_engagement_type import MeetingEngagementType
from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MeetingEngagement(ClientValue):
    dateTime: datetime | None = None
    engagementSubType: str | None = None
    engagementType: MeetingEngagementType = MeetingEngagementType.reaction

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MeetingEngagement"
