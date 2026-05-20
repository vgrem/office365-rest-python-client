from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class SocialFeedOptions(ClientValue):
    MaxThreadCount: Optional[int] = None
    NewerThan: Optional[datetime] = None
    OlderThan: Optional[datetime] = None
    SortOrder: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFeedOptions"
