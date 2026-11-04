from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MicrofeedLinkAction(ClientValue):
    ActionUri: Optional[str] = None
    Height: Optional[int] = None
    Kind: Optional[int] = None
    Width: Optional[int] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedLinkAction"
