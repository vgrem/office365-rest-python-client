from typing import Optional

from office365.runtime.client_value import ClientValue


class WebInfoCreationInformation(ClientValue):
    def __init__(
        self,
        description: Optional[str] = None,
        language: Optional[int] = None,
        title: Optional[str] = None,
        url: Optional[str] = None,
        use_unique_permissions: Optional[bool] = None,
        web_template: Optional[str] = None,
    ):
        super().__init__()
        self.Description = description
        self.Language = language
        self.Title = title
        self.Url = url
        self.UseUniquePermissions = use_unique_permissions
        self.WebTemplate = web_template
