from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.directory.provider.link_change import LinkChange
from office365.sharepoint.directory.provider.property_change import PropertyChange


@dataclass
class DirectoryObjectChanges(ClientValue):
    DirectoryObjectSubType: Optional[int] = None
    DirectoryObjectType: Optional[int] = None
    Id: Optional[str] = None
    LinkChanges: ClientValueCollection[LinkChange] = field(default_factory=lambda: ClientValueCollection(LinkChange))
    PropertyChanges: ClientValueCollection[PropertyChange] = field(
        default_factory=lambda: ClientValueCollection(PropertyChange)
    )

    @property
    def entity_type_name(self):
        return "SP.Directory.Provider.DirectoryObjectChanges"
