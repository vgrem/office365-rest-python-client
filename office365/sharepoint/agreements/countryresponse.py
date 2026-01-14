from office365.runtime.client_value import ClientValue


class AgreementCountryResponse(ClientValue):
    def __init__(self, country_key: str = None, display_name: str = None):
        self.country_key = country_key
        self.display_name = display_name
