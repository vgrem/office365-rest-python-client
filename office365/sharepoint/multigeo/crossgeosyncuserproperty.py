from office365.runtime.client_value import ClientValue


class CrossGeoSyncUserProperty(ClientValue):

    def __init__(
        self,
        ds_guid: str = None,
        is_multivalue: bool = None,
        privacy: int = None,
        property_id: int = None,
        property_val: str = None,
        secondary_val: str = None,
    ):
        self.DsGuid = ds_guid
        self.IsMultivalue = is_multivalue
        self.Privacy = privacy
        self.PropertyId = property_id
        self.PropertyVal = property_val
        self.SecondaryVal = secondary_val
