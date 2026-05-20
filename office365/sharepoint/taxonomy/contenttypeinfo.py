from dataclasses import dataclass
from typing import Optional

from office365.runtime.client_value import ClientValue


@dataclass
class ContentTypeInfo(ClientValue):
    Description: Optional[str] = None
    Group: Optional[str] = None
    Id: Optional[str] = None
    IsHidden: Optional[bool] = None
    IsSealed: Optional[bool] = None
    Name: Optional[str] = None
    ParentName: Optional[str] = None

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.ContentTypeSync.ContentTypeInfo"
