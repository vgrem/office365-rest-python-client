from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
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
