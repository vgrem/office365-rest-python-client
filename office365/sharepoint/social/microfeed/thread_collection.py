from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.social.microfeed.thread import MicrofeedThread


@dataclass
class MicrofeedThreadCollection(ClientValue):
    CurrentUserUnreadMentionCount: Optional[int] = None
    NewestProcessed: Optional[datetime] = None
    OldestProcessed: Optional[datetime] = None
    Items: ClientValueCollection[MicrofeedThread] = field(default_factory=lambda: ClientValueCollection(MicrofeedThread))

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedThreadCollection"
