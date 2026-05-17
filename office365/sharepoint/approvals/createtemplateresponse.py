from typing import Optional

from office365.runtime.client_value import ClientValue


class CreateTemplateResponse(ClientValue):
    def __init__(
        self,
        server_relative_url: Optional[str] = None,
        title: Optional[str] = None,
        unique_id: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.ServerRelativeUrl = server_relative_url
        self.Title = title
        self.UniqueID = unique_id
        self.Url = url
