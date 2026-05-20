from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SPRuleUserInfo(ClientValue):
    name: Optional[str] = None
    user_id: Optional[int] = None
