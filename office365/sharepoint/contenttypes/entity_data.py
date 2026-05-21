from __future__ import annotations


from dataclasses import dataclass
from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeEntityData(ClientValue):

    Name = None
    Description = None
    Group = None
    ParentContentTypeId = None

    @property
    def entity_type_name(self):
        return "SP.ContentTypeEntityData"