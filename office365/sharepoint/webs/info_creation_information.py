from office365.runtime.client_value import ClientValue


class WebInfoCreationInformation(ClientValue):
    def __init__(
        self,
        description: str = None,
        language: int = None,
        title: str = None,
        url: str = None,
        use_unique_permissions: bool = None,
        web_template: str = None,
    ):
        super().__init__()
        self.Description = description
        self.Language = language
        self.Title = title
        self.Url = url
        self.UseUniquePermissions = use_unique_permissions
        self.WebTemplate = web_template
