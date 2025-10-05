from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.multigeo.crossgeosyncuserproperty import (
    CrossGeoSyncUserProperty,
)


class CrossGeoSyncUserDataBatch(ClientValue):

    def __init__(
        self,
        last_event_id: int = None,
        last_record_id: int = None,
        properties: ClientValueCollection[
            CrossGeoSyncUserProperty
        ] = ClientValueCollection(CrossGeoSyncUserProperty),
    ):
        self.LastEventId = last_event_id
        self.LastRecordId = last_record_id
        self.Properties = properties

    ""

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.CrossGeoSyncUserDataBatch"
