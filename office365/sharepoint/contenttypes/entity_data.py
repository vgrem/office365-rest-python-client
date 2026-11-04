from __future__ import annotations

from typing import Optional

from office365.runtime.client_value import ClientValue
from office365.runtime.types.value import value


@value
class ContentTypeEntityData(ClientValue):
    Name: Optional[str] = None
    Description: Optional[str] = None
    Group: Optional[str] = None
    ParentContentTypeId: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.ContentTypeEntityData"
