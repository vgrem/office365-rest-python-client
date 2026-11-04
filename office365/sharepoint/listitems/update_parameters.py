from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ListItemUpdateParameters(ClientValue):
    BypassQuotaCheck: bool | None = None
    BypassSharedLock: bool | None = None
