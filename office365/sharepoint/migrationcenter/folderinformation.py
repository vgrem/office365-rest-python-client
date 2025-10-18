from office365.runtime.client_value import ClientValue


class SPFolderInformation(ClientValue):

    def __init__(
        self,
        depth: int = None,
        is_specified: bool = None,
        name: str = None,
        server_relative_url: str = None,
        web_relative_url: str = None,
    ):
        self.Depth = depth
        self.IsSpecified = is_specified
        self.Name = name
        self.ServerRelativeUrl = server_relative_url
        self.WebRelativeUrl = web_relative_url

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.SPFolderInformation"
