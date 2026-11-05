from typing import Optional

from office365.runtime.client_value import ClientValue


class AcronymInformation(ClientValue):
    Acronym: Optional[str] = None
    Color: Optional[str] = None
    Lcid: Optional[int] = None
    Text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.AcronymInformation"
