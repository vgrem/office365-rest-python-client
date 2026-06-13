from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class CrossGeoSyncUserProperty(ClientValue):
    DsGuid: Optional[str] = None
    IsMultivalue: Optional[bool] = None
    Privacy: Optional[int] = None
    PropertyId: Optional[int] = None
    PropertyVal: Optional[str] = None
    SecondaryVal: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.CrossGeoSyncUserProperty"
