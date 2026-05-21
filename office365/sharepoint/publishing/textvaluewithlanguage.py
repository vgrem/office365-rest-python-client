from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TextValueWithLanguage(ClientValue):
    ColorSeed: Optional[str] = None
    Lcid: Optional[int] = None
    Text: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.TextValueWithLanguage"
