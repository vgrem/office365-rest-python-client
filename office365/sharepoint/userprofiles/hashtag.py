from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class Hashtag(ClientValue):
    def __init__(
        self,
        actor: Optional[str] = None,
        application: Optional[str] = None,
        label: Optional[str] = None,
        timestamp: datetime = datetime.min,
    ):
        self.actor = actor
        self.application = application
        self.label = label
        self.timestamp = timestamp
