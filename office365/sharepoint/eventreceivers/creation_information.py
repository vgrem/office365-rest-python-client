from typing import Optional

from office365.runtime.client_value import ClientValue


class EventReceiverCreationInformation(ClientValue):
    def __init__(
        self,
        receiver_name: Optional[str] = None,
        receiver_assembly: Optional[str] = None,
        receiver_class: Optional[str] = None,
        receiver_url: Optional[str] = None,
        event_type: Optional[int] = None,
        receiver_id: Optional[int] = None,
        synchronization: Optional[str] = None,
        sequence_number: int = 0,
    ):
        """Event receiver creation information"""
        super().__init__()
        self.ReceiverName = receiver_name
        self.ReceiverAssembly = receiver_assembly
        self.ReceiverClass = receiver_class
        self.ReceiverUrl = receiver_url
        self.EventType = event_type
        self.ReceiverId = receiver_id
        self.Synchronization = synchronization
        self.SequenceNumber = sequence_number
