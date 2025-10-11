from office365.directory.security.triggertypes.event_type import RetentionEventType
from office365.entity_collection import EntityCollection


class RetentionEventTypeCollection(EntityCollection[RetentionEventType]):
    """"""

    def __init__(self, context, resource_path=None):
        super(RetentionEventTypeCollection, self).__init__(context, RetentionEventType, resource_path)
