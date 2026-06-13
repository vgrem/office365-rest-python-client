from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.multigeo.service.crossgeosyncuserproperty import (
    CrossGeoSyncUserProperty,
)


@dataclass
class CrossGeoSyncUserDataBatch(ClientValue):
    LastEventId: Optional[int] = None
    LastRecordId: Optional[int] = None
    Properties: ClientValueCollection[CrossGeoSyncUserProperty] = field(
        default_factory=lambda: ClientValueCollection(CrossGeoSyncUserProperty)
    )

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.CrossGeoSyncUserDataBatch"
