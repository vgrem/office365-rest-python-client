from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class FontOption(ClientValue):
    font_face: Optional[str] = None
    font_family_key: Optional[str] = None
    font_variant_weight: Optional[str] = None
