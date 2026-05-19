from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.sharepoint.clientsidecomponent.updatecardelement import UpdateCardElement


@dataclass
class ElementUpdate(ClientValue):
    action: str | None = None
    element: UpdateCardElement = field(default_factory=UpdateCardElement)
    element_id: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.ElementUpdate"
