from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.clientsidecomponent.elementupdate import ElementUpdate


@dataclass
class UpdateCard(ClientValue):
    card_updates: ClientValueCollection[ElementUpdate] = field(
        default_factory=lambda: ClientValueCollection(ElementUpdate)
    )
    type_: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCard"
