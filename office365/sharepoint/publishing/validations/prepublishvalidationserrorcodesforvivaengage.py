from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.viva.destinationv2 import VivaEngageDestinationV2


class PrePublishValidationsErrorCodesForVivaEngage(ClientValue):

    def __init__(
        self,
        destination_name: str = None,
        destination_type: int = None,
        error_codes: ClientValueCollection[int] = ClientValueCollection(int),
        number_of_image_attachments: int = None,
        viva_engage_destination_v2: VivaEngageDestinationV2 = VivaEngageDestinationV2(),
    ):
        self.DestinationName = destination_name
        self.DestinationType = destination_type
        self.ErrorCodes = error_codes
        self.NumberOfImageAttachments = number_of_image_attachments
        self.VivaEngageDestinationV2 = viva_engage_destination_v2
