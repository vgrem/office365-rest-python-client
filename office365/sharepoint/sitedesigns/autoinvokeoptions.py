from typing import Optional

from office365.runtime.client_value import ClientValue


class AutoInvokeOptions(ClientValue):
    showCardOnFailure: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.QuickActionMessageCard.AutoInvokeOptions"
