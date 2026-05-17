from office365.runtime.client_value import ClientValue
from typing import Optional


class CrossGeoSyncUserProperty(ClientValue):
    def __init__(
        self,
        ds_guid: Optional[str] = None,
        is_multivalue: Optional[bool] = None,
        privacy: Optional[int] = None,
        property_id: Optional[int] = None,
        property_val: Optional[str] = None,
        secondary_val: Optional[str] = None,
    ):
        self.DsGuid = ds_guid
        self.IsMultivalue = is_multivalue
        self.Privacy = privacy
        self.PropertyId = property_id
        self.PropertyVal = property_val
        self.SecondaryVal = secondary_val

    @property
    def entity_type_name(self):
        return "SP.UserProfiles.CrossGeoSyncUserProperty"
