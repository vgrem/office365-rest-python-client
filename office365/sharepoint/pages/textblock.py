from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class TextBlock(ClientValue):
    color: Optional[str] = None
    horizontal_alignment: Optional[str] = None
    size: Optional[str] = None
    text: Optional[str] = None
    weight: Optional[str] = None
    wrap: Optional[bool] = None
