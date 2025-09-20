from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class PlaceholderV2(ClientValue):
    pass


class ContentAssemblyModernTemplateColumnsMappingInfo(ClientValue):

    def __init__(
        self,
        destination_list_content_type_id: str = None,
        destination_site_content_type_id: str = None,
        placeholders: ClientValueCollection[PlaceholderV2] = ClientValueCollection[
            PlaceholderV2
        ],
    ):
        self.destination_list_content_type_id = destination_list_content_type_id
        self.destination_site_content_type_id = destination_site_content_type_id
        self.placeholders = placeholders
