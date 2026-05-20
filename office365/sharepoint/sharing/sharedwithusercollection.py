from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.sharing.shared_with_user import SharedWithUser


@dataclass
class SharedWithUserCollection(ClientValue):
    items: ClientValueCollection[SharedWithUser] = field(default_factory=lambda: ClientValueCollection(SharedWithUser))
