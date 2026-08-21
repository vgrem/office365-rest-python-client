from office365.runtime.paths.service_operation import ServiceOperationPath
from office365.runtime.queries.create_entity import CreateEntityQuery
from office365.sharepoint.entity_collection import EntityCollection
from office365.sharepoint.eventreceivers.definition import EventReceiverDefinition


class EventReceiverDefinitionCollection(EntityCollection[EventReceiverDefinition]):
    """
    Represents a collection of SP.EventReceiverDefinition objects that are used to enumerate the list of
    registered event receivers for Windows SharePoint Services objects that can have events.
    """

    def __init__(self, context, resource_path=None, parent=None):
        """Represents a collection of SP.EventReceiverDefinition objects that are used to enumerate the list of
        registered event receivers for Windows SharePoint Services objects that can have events.
        """
        super().__init__(context, EventReceiverDefinition, resource_path, parent)

    def add(
        self,
        receiver_name: str,
        receiver_url: str,
        event_type: int = 2,          # EventReceiverType: 2 = ItemAdded
        synchronization: int = 1,     # EventReceiverSynchronization: 1 = Asynchronous
        sequence_number: int = 1000,
        **kwargs,
    ) -> EventReceiverDefinition:
        """Add a new event receiver to the collection (deferred — call ``execute_query()`` to submit).

        Args:
            receiver_name: The name of the event receiver.
            receiver_url: The URL of the event receiver endpoint.
            event_type: The event type (2 = ItemAdded).
            synchronization: Whether the receiver runs synchronously or asynchronously (1 = Asynchronous).
            sequence_number: The order in which the receiver is executed.
        """
        return_type = EventReceiverDefinition(self.context)
        return_type.set_property("ReceiverName", receiver_name)
        return_type.set_property("ReceiverUrl", receiver_url)
        return_type.set_property("EventType", event_type)
        return_type.set_property("Synchronization", synchronization)
        return_type.set_property("SequenceNumber", sequence_number)
        for k, v in kwargs.items():
            return_type.set_property(k, v)
        self.add_child(return_type)
        qry = CreateEntityQuery(self, return_type, return_type)
        self.context.add_query(qry)
        return return_type

    def get_by_id(self, event_receiver_id: str) -> EventReceiverDefinition:
        """Returns the event receiver with the specified identifier.

        Args:
            event_receiver_id (str): The identifier of the event receiver.
        """
        return EventReceiverDefinition(
            self.context,
            ServiceOperationPath("GetById", [event_receiver_id], self.resource_path),
        )
