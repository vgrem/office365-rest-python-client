from office365.runtime.client_value import ClientValue


class CreateTemplateResponse(ClientValue):

    def __init__(
        self,
        server_relative_url: str = None,
        title: str = None,
        unique_id: str = None,
        url: str = None,
    ):
        self.ServerRelativeUrl = server_relative_url
        self.Title = title
        self.UniqueID = unique_id
        self.Url = url
