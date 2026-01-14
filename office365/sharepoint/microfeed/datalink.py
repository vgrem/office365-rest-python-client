from datetime import datetime

from office365.runtime.client_value import ClientValue


class MicrofeedDataLink(ClientValue):
    def __init__(
        self,
        data_link_type: int = None,
        date_time_value: datetime = None,
        name: str = None,
        place_holder_name: str = None,
        string_value: str = None,
        unique_id: str = None,
        uri_value: str = None,
    ):
        self.DataLinkType = data_link_type
        self.DateTimeValue = date_time_value
        self.Name = name
        self.PlaceHolderName = place_holder_name
        self.StringValue = string_value
        self.UniqueId = unique_id
        self.UriValue = uri_value

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataLink"
