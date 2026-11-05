from typing import Optional

from office365.runtime.client_value import ClientValue


class PageDeepCopyWarning(ClientValue):
    WarningMessage: Optional[str] = None
    WarningType: Optional[int] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Publishing.PageCopyWithAssets.PageDeepCopyWarning"
