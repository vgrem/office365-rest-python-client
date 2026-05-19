from __future__ import annotations

from dataclasses import dataclass

from office365.runtime.client_value import ClientValue


@dataclass
class UpdateCardElement(ClientValue):
    is_visible: bool | None = None
    type_: str | None = None
    value: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCardElement"
