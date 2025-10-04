from office365.runtime.client_value import ClientValue


class SendTestTeamsMessageResponse(ClientValue):

    def __init__(self, error_code: int = None, response: bool = None):
        self.ErrorCode = error_code
        self.Response = response
