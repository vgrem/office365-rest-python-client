from typing import Optional

from office365.runtime.client_value import ClientValue


class FontOption(ClientValue):
    def __init__(
        self,
        font_face: Optional[str] = None,
        font_family_key: Optional[str] = None,
        font_variant_weight: Optional[str] = None,
    ):
        self.font_face = font_face
        self.font_family_key = font_family_key
        self.font_variant_weight = font_variant_weight
