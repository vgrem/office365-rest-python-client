from dataclasses import dataclass
from datetime import time
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentAnchor(ClientValue):
    timelineOffset: Optional[time] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Comments.ContentAnchor"
