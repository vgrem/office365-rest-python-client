from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MissingSharePointDestinationWebIdRepairItem(ClientValue):
    SiteId: Optional[str] = None
    SiteUrl: Optional[str] = None
    WebId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Publishing.MissingSharePointDestinationWebIdRepairItem"
