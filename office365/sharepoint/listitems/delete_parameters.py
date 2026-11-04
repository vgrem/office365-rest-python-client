from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ListItemDeleteParameters(ClientValue):
    """Args:
    bypass_shared_lock (bool):
    """

    BypassSharedLock: bool | None = None
