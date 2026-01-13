from office365.runtime.client_value import ClientValue


class WebInfoCreationInformation(ClientValue):
    def __init__(self, description=None, language=None):
        super(WebInfoCreationInformation, self).__init__()
        self.Description = description
        self.Language = language
