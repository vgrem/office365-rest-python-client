from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


class SocialFeedOptions(ClientValue):
    MaxThreadCount: Optional[int] = None
    NewerThan: Optional[datetime] = None
    OlderThan: Optional[datetime] = None
    SortOrder: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Social.SocialFeedOptions"
