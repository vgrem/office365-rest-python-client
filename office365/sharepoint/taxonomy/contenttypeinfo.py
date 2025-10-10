from office365.runtime.client_value import ClientValue


class ContentTypeInfo(ClientValue):

    def __init__(
        self,
        description: str = None,
        group: str = None,
        id_: str = None,
        is_hidden: bool = None,
        is_sealed: bool = None,
        name: str = None,
        parent_name: str = None,
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
