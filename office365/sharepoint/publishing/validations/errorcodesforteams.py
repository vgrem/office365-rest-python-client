from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class PrePublishValidationsErrorCodesForTeams(ClientValue):

    def __init__(
        self,
        audience_id: str = None,
        error_codes: ClientValueCollection[int] = ClientValueCollection(int),
        number_of_images_in_payload: int = None,
    ):
        self.AudienceId = audience_id
        self.ErrorCodes = error_codes
        self.NumberOfImagesInPayload = number_of_images_in_payload

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForTeams"
