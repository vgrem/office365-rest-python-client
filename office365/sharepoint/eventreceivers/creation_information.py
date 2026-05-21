from __future__ import annotations

from typing import Optional


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class EventReceiverCreationInformation(ClientValue):

    """Event receiver creation information"""

    ReceiverName: Optional[str] = None
    ReceiverAssembly: Optional[str] = None
    ReceiverClass: Optional[str] = None
    ReceiverUrl: Optional[str] = None
    EventType: Optional[int] = None
    ReceiverId: Optional[int] = None
    Synchronization: Optional[str] = None
    SequenceNumber: int = 0