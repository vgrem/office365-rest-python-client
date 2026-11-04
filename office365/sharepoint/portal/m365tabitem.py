from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class M365TabItem(ClientValue):
    displayName: Optional[str] = None
    isDefault: Optional[bool] = None
    itemType: Optional[int] = None
    url: Optional[str] = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.M365TabItem"
