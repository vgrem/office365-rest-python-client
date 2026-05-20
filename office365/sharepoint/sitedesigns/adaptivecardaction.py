from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class AdaptiveCardAction(ClientValue):
    is_primary: Optional[bool] = None
    title: Optional[str] = None
