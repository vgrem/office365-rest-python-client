from typing import Optional

from office365.runtime.client_value import ClientValue


class Choice(ClientValue):
    display: Optional[str] = None
    value: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.Choice"
