from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPResourceEntry(ClientValue):
    LCID: Optional[int] = None
    Value: Optional[str] = None
