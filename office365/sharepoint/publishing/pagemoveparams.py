from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class PageMoveParams(ClientValue):
    DestinationWebUrl: Optional[str] = None
    ShouldPublish: Optional[bool] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.PageMoveParams"
