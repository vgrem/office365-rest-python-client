from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.types.value import value
from office365.teams.teamwork.meeting_note_subpoint import MeetingNoteSubpoint


@value
class MeetingNote(ClientValue):
    subpoints: ClientValueCollection[MeetingNoteSubpoint] = field(
        default_factory=lambda: ClientValueCollection(MeetingNoteSubpoint)
    )
    text: str | None = None
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MeetingNote"
