from office365.runtime.client_value import ClientValue


class SiteSharingEmailContext(ClientValue):

    def __init__(
        self,
        custom_description: str = None,
        custom_title: str = None,
        message: str = None,
        url: str = None,
    ):
        self.CustomDescription = custom_description
        self.CustomTitle = custom_title
        self.Message = message
        self.Url = url
