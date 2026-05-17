from typing import Optional

from office365.runtime.client_value import ClientValue


class TextValueWithLanguage(ClientValue):
    def __init__(self, color_seed: Optional[str] = None, lcid: Optional[int] = None, text: Optional[str] = None):
        self.ColorSeed = color_seed
        self.Lcid = lcid
        self.Text = text

    @property
    def entity_type_name(self):
        return "SP.Publishing.TextValueWithLanguage"
