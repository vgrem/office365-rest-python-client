from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from office365.common.meeting_engagement_type import MeetingEngagementType
from office365.runtime.client_value import ClientValue


@dataclass
class MeetingEngagement(ClientValue):
    dateTime: datetime | None = None
    engagementSubType: str | None = None
    engagementType: MeetingEngagementType = MeetingEngagementType.reaction

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MeetingEngagement"
