from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection


@dataclass
class SPMoveAndShareFileInfo(ClientValue):
    item_permissionable_user_ids: ClientValueCollection[int] = field(default_factory=lambda: ClientValueCollection(int))
