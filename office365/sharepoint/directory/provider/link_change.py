from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.directory.linktarget import LinkTarget


@dataclass
class LinkChange(ClientValue):
    Added: ClientValueCollection[LinkTarget] = field(default_factory=lambda: ClientValueCollection(LinkTarget))
    Name: Optional[str] = None
    Removed: ClientValueCollection[LinkTarget] = field(default_factory=lambda: ClientValueCollection(LinkTarget))

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.LinkChange"
