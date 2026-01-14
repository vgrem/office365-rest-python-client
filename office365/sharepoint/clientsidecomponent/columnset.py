from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.adaptivecardcolumn import (
    AdaptiveCardColumn,
)
from office365.sharepoint.clientsidecomponent.padding import Padding


class ColumnSet(ClientValue):
    def __init__(
        self,
        columns: ClientValueCollection[AdaptiveCardColumn] = ClientValueCollection(AdaptiveCardColumn),
        horizontal_alignment: str = None,
        padding: Padding = Padding(),
    ):
        self.columns = columns
        self.horizontal_alignment = horizontal_alignment
        self.padding = padding
