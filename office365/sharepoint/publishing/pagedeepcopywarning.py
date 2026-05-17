from typing import Optional

from office365.runtime.client_value import ClientValue


class PageDeepCopyWarning(ClientValue):
    def __init__(self, warning_message: Optional[str] = None, warning_type: Optional[int] = None):
        self.WarningMessage = warning_message
        self.WarningType = warning_type

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.PageCopyWithAssets.PageDeepCopyWarning"
