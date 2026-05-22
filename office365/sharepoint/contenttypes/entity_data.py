from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeEntityData(ClientValue):
    Name: Optional[str] = None
    Description: Optional[str] = None
    Group: Optional[str] = None
    ParentContentTypeId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ContentTypeEntityData"
