from typing import Optional

from office365.runtime.client_value import ClientValue


class SiteSharingEmailContext(ClientValue):
    def __init__(
        self,
        custom_description: Optional[str] = None,
        custom_title: Optional[str] = None,
        message: Optional[str] = None,
        url: Optional[str] = None,
    ):
        self.CustomDescription = custom_description
        self.CustomTitle = custom_title
        self.Message = message
        self.Url = url

    @property
    def entity_type_name(self):
        return "SP.Publishing.SiteSharingEmailContext"
