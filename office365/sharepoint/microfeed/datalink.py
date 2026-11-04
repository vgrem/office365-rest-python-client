from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class MicrofeedDataLink(ClientValue):
    DataLinkType: Optional[int] = None
    DateTimeValue: Optional[datetime] = None
    Name: Optional[str] = None
    PlaceHolderName: Optional[str] = None
    StringValue: Optional[str] = None
    UniqueId: Optional[str] = None
    UriValue: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Microfeed.MicrofeedDataLink"
