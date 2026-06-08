from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemDeleteParameters(ClientValue):
    """Args:
        bypass_shared_lock (bool):
    """

    BypassSharedLock: bool | None = None
