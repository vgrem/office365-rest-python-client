from office365.runtime.client_value import ClientValue


class AcronymInformation(ClientValue):

    def __init__(
        self, acronym: str = None, color: str = None, lcid: int = None, text: str = None
    ):
        self.Acronym = acronym
        self.Color = color
        self.Lcid = lcid
        self.Text = text
