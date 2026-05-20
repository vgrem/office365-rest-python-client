from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SensitivityLabelInfo(ClientValue):
    display_name: Optional[str] = None
    id: Optional[str] = None
    members_can_share: Optional[str] = None
