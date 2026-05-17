from office365.runtime.client_value import ClientValue
from typing import Optional


class Choice(ClientValue):
    def __init__(self, display: Optional[str] = None, value: Optional[str] = None):
        self.display = display
        self.value = value

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.Choice"
