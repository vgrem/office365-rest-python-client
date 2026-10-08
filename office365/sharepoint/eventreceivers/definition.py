from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class EventReceiverDefinition(Entity):
    """Abstract base class that defines general properties of an event receiver for list items, lists,
    websites, and workflows."""

    @property
    def receiver_assembly(self) -> Optional[str]:
        """Specifies the strong name of the assembly that is used for the event receiver."""
        return self.properties.get("ReceiverAssembly", None)

    @property
    def receiver_class(self) -> Optional[str]:
        """Specifies the strong name of the assembly that is used for the event receiver."""
        return self.properties.get("ReceiverClass", None)

    @property
    def receiver_url(self) -> Optional[str]:
        """Gets the URL of the receiver for the event."""
        return self.properties.get("ReceiverUrl", None)

    @property
    def receiver_id(self) -> Optional[UUID]:
        """Gets the ReceiverId property"""
        return self.properties.get("ReceiverId", None)

    @property
    def receiver_name(self) -> Optional[str]:
        """Gets the ReceiverName property"""
        return self.properties.get("ReceiverName", None)

    @property
    def sequence_number(self) -> Optional[int]:
        """Gets the SequenceNumber property"""
        return self.properties.get("SequenceNumber", None)

    @property
    def synchronization(self) -> Optional[int]:
        """Gets the Synchronization property"""
        return self.properties.get("Synchronization", None)

    @property
    def event_type(self) -> Optional[int]:
        """Gets the EventType property"""
        return self.properties.get("EventType", None)
