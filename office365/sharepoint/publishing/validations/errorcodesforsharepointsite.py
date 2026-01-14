from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class PrePublishValidationsErrorCodesForSharePointSite(ClientValue):
    def __init__(
        self,
        error_codes: ClientValueCollection[int] = ClientValueCollection(int),
        site_id: str = None,
    ):
        self.ErrorCodes = error_codes
        self.SiteId = site_id

    @property
    def entity_type_name(self):
        return "SP.Publishing.PrePublishValidationsErrorCodesForSharePointSite"
