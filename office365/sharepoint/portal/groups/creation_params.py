from typing import List

from office365.runtime.client_value import ClientValue
from office365.runtime.types.collections import StringCollection


class GroupCreationParams(ClientValue):
    """Group creation params"""

    def __init__(
        self,
        creation_options: List[str] = None,
        classification: str = "",
        description: str = "",
        owners: List[str] = None,
        preferred_data_location: str = None,
    ):
        super().__init__()
        if creation_options is None:
            creation_options = ["SPSiteLanguage:1033"]
        self.Classification = classification
        self.Description = description
        self.CreationOptions = StringCollection(creation_options)
        self.Owners = StringCollection(owners)
        self.PreferredDataLocation = preferred_data_location

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Portal.GroupCreationParams"
