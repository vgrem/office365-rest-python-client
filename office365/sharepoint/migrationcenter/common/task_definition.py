from office365.runtime.client_value import ClientValue


class MigrationTaskDefinition(ClientValue):
    def __init__(
        self,
        name=None,
        source_list_name=None,
        source_list_relative_path=None,
        source_uri=None,
        source_user_name=None,
        target_list_name=None,
        target_list_relative_path: str = None,
        target_site_url: str = None,
        target_user_name: str = None,
        type_: int = None,
    ):
        self.Name = name
        self.SourceListName = source_list_name
        self.SourceListRelativePath = source_list_relative_path
        self.SourceUri = source_uri
        self.SourceUserName = source_user_name
        self.TargetListName = target_list_name
        self.TargetListRelativePath = target_list_relative_path
        self.TargetSiteUrl = target_site_url
        self.TargetUserName = target_user_name
        self.Type = type_

    @property
    def entity_type_name(self) -> str:
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.MigrationTaskDefinition"
