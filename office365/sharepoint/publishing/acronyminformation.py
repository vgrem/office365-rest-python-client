from typing import Optional

from office365.runtime.client_value import ClientValue


class AcronymInformation(ClientValue):
    def __init__(
        self,
        acronym: Optional[str] = None,
        color: Optional[str] = None,
        lcid: Optional[int] = None,
        text: Optional[str] = None,
    ):
        self.Acronym = acronym
        self.Color = color
        self.Lcid = lcid
        self.Text = text

    @property
    def entity_type_name(self):
        return "SP.Publishing.AcronymInformation"
