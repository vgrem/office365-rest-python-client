from typing import Optional

from office365.runtime.client_value import ClientValue


class ListCollectionPosition(ClientValue):
    """Fields:
    PagingInfo (str):
    """

    PagingInfo: Optional[str] = "Paged=TRUE&p_ID=0"

    @property
    def entity_type_name(self):
        return "SP.ListCollectionPosition"
