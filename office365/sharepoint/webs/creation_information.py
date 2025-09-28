from office365.runtime.client_value import ClientValue


class WebCreationInformation(ClientValue):
    """Represents metadata about site creation."""

    def __init__(
        self,
        description: str = None,
        language: int = None,
        title: str = None,
        url: str = None,
        use_same_permissions_as_parent_site: bool = None,
        web_template: str = None,
    ):
        super().__init__()
        self.Title = None
        self.Url = None
        self.Description = description
        self.Language = language
        self.Title = title
        self.Url = url
        self.UseSamePermissionsAsParentSite = use_same_permissions_as_parent_site
        self.WebTemplate = web_template

    @property
    def entity_type_name(self):
        return "SP.WebCreationInformation"
