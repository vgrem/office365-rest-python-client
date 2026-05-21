from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class MissingSharePointDestinationWebIdRepairItem(ClientValue):
    SiteId: Optional[str] = None
    SiteUrl: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.MissingSharePointDestinationWebIdRepairItem"
