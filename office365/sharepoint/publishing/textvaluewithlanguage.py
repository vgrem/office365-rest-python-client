from typing import Optional

from office365.runtime.client_value import ClientValue


class TextValueWithLanguage(ClientValue):
    ColorSeed: Optional[str] = None
    Lcid: Optional[int] = None
    Text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TextValueWithLanguage"
