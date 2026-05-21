from __future__ import annotations

from dataclasses import dataclass, field

from office365.outlook.calendar.meetingtimes.suggestion import MeetingTimeSuggestion
from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class MeetingTimeSuggestionsResult(ClientValue):
    """
    A collection of meeting suggestions if there is any, or the reason if there isn't.
    """

    meetingTimeSuggestions: ClientValueCollection = field(
        default_factory=lambda: ClientValueCollection(MeetingTimeSuggestion)
    )
    emptySuggestionsReason: str | None = None
