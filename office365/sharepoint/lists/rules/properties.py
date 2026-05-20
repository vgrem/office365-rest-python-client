from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class RulesProperties(ClientValue):
    RulesKey: Optional[str] = None
    RulesValue: Optional[str] = None
