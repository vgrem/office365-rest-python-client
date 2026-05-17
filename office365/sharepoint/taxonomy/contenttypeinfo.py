from typing import Optional

from office365.runtime.client_value import ClientValue


class ContentTypeInfo(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        group: Optional[str] = None,
        id_: Optional[str] = None,
        is_hidden: Optional[bool] = None,
        is_sealed: Optional[bool] = None,
        name: Optional[str] = None,
        parent_name: Optional[str] = None,
    ):
        self.Description = description
        self.Group = group
        self.Id = id_
        self.IsHidden = is_hidden
        self.IsSealed = is_sealed
        self.Name = name
        self.ParentName = parent_name

    @property
    def entity_type_name(self):
        return "SP.Taxonomy.ContentTypeSync.ContentTypeInfo"
