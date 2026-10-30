from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from office365.communications.callrecords.session import Session
from office365.communications.callrecords.type import CallType
from office365.communications.calls.organizer import Organizer
from office365.communications.calls.participant import Participant
from office365.communications.quotas import CALL_RECORD_BUDGETS, CALL_RECORD_RESOURCE_QUOTA
from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.client_value_collection import ClientValueCollection
from office365.runtime.limits import limit
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.callrecords.modality import Modality


@limit(*CALL_RECORD_BUDGETS)
class CallRecord(Entity):
    """Represents a single peer-to-peer call or a group call between multiple participants,
    sometimes referred to as an online meeting."""

    @odata(name="joinWebUrl")
    @property
    def join_web_url(self) -> Optional[str]:
        """Meeting URL associated to the call. May not be available for a peerToPeer call record type."""
        return self.properties.get("joinWebUrl", None)

    @odata(name="organizer")
    @property
    def organizer(self) -> IdentitySet:
        """The organizing party's identity.."""
        return self.properties.get("organizer", IdentitySet())

    @odata(name="sessions", navigation=True)
    @property
    @limit(CALL_RECORD_RESOURCE_QUOTA)
    def sessions(self) -> EntityCollection[Session]:
        """
        List of sessions involved in the call. Peer-to-peer calls typically only have one session, whereas group
        calls typically have at least one session per participant.
        """
        return self.properties.get(
            "sessions", EntityCollection(self.context, Session, ResourcePath("sessions", self.resource_path))
        )

    @odata(name="endDateTime")
    @property
    def end_date_time(self) -> datetime:
        """Gets the endDateTime property"""
        return self.properties.get("endDateTime", datetime.min)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> datetime:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", datetime.min)

    @odata(name="participants")
    @property
    def participants(self) -> ClientValueCollection[IdentitySet]:
        """Gets the participants property"""
        return self.properties.get("participants", ClientValueCollection[IdentitySet](IdentitySet))

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> datetime:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="type")
    @property
    def type_(self) -> CallType:
        """Gets the type property"""
        return self.properties.get("type", CallType.unknown)

    @odata(name="version")
    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @odata(name="organizer_v2", navigation=True)
    @property
    def organizer_v2(self) -> Organizer:
        """Gets the organizer_v2 property"""
        return self.properties.get(
            "organizer_v2", Organizer(self.context, ResourcePath("organizer_v2", self.resource_path))
        )

    @odata(name="participants_v2", navigation=True)
    @property
    @limit(CALL_RECORD_RESOURCE_QUOTA)
    def participants_v2(self) -> EntityCollection[Participant]:
        """Gets the participants_v2 property"""
        return self.properties.get(
            "participants_v2",
            EntityCollection[Participant](
                self.context, Participant, ResourcePath("participants_v2", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.callRecords.CallRecord"

    @odata(name="modalities")
    @property
    def modalities(self) -> ClientValueCollection[Modality]:
        """Gets the modalities property"""
        from office365.communications.callrecords.modality import Modality

        return self.properties.get("modalities", ClientValueCollection[Modality](Modality))
