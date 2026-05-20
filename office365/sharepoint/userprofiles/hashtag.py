from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class Hashtag(ClientValue):
    actor: Optional[str] = None
    application: Optional[str] = None
    label: Optional[str] = None
    timestamp: datetime = datetime.min
