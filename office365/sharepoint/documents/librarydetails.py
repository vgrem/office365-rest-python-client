from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class LibraryDetails(ClientValue):
    BaseTemplateType: Optional[int] = None
    IsApprovalsEnabled: Optional[bool] = None
    ListId: Optional[str] = None
    ListItemEntityTypeFullName: Optional[str] = None
    ListName: Optional[str] = None
