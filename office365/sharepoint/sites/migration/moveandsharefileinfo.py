from __future__ import annotations

from dataclasses import field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


class SPMoveAndShareFileInfo(ClientValue):
    ItemPermissionableUserIds: ClientValueCollection = field(default_factory=ClientValueCollection)
