from __future__ import annotations

from office365.runtime.client_value import ClientValue


class ListItemUpdateParameters(ClientValue):
    BypassQuotaCheck: bool | None = None
    BypassSharedLock: bool | None = None
