from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.calls.participant import Participant


class DeltaParticipants(Entity):
    @odata(name="sequenceNumber")
    @property
    def sequence_number(self) -> Optional[int]:
        """Gets the sequenceNumber property"""
        return self.properties.get("sequenceNumber", None)

    @odata(name="participants", navigation=True)
    @property
    def participants(self) -> EntityCollection[Participant]:
        """Gets the participants property"""
        from office365.communications.calls.participant import Participant

        return self.properties.get(
            "participants",
            EntityCollection[Participant](self.context, Participant, ResourcePath("participants", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.DeltaParticipants"
