from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ActionOpenUrl(ClientValue):
    url: Optional[str] = None
