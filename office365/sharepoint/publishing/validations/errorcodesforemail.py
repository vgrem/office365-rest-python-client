from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class PrePublishValidationsErrorCodesForEmail(ClientValue):

    def __init__(
        self,
        email_address: str = None,
        error_codes: ClientValueCollection[int] = ClientValueCollection(int),
    ):
        self.EmailAddress = email_address
        self.ErrorCodes = error_codes
