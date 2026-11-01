from office365.entity_collection import EntityCollection
from office365.runtime.query_capabilities import query_capabilities
from office365.security.triggertypes.event_type import RetentionEventType

_DOC = "https://learn.microsoft.com/en-us/graph/api/security-triggertypes-list"


@query_capabilities(
    unsupported={"top", "skip", "order_by", "filter", "select"},
    doc=_DOC,
    note="the retention feed rejects every standard query option",
)
class RetentionEventTypeCollection(EntityCollection[RetentionEventType]):
    """"""

    def __init__(self, context, resource_path=None):
        super().__init__(context, RetentionEventType, resource_path)
