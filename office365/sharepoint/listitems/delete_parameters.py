from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class ListItemDeleteParameters(ClientValue):
    """
    :param bool bypass_shared_lock:
    """

    BypassSharedLock: bool | None = None
