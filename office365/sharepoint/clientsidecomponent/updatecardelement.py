from __future__ import annotations

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class UpdateCardElement(ClientValue):
    is_visible: bool | None = None
    type_: str | None = None
    value: str | None = None
    isVisible: bool | None = None
    type: str | None = None

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.ActionableMessage.UpdateCardElement"
