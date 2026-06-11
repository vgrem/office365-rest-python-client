from __future__ import annotations

from office365.runtime.client_value import ClientValue


class EventReceiverDefinitionCreationInformation(ClientValue):
    ReceiverAssembly: str | None = None
    ReceiverClass: str | None = None
    ReceiverName: str | None = None
    SequenceNumber: int | None = None
    Synchronization: int | None = None
    EventType: int | None = None
    ReceiverUrl: str | None = None
