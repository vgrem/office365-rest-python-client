from uuid import UUID

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.sharepoint.migrationcenter.spfolderinformation import SPFolderInformation


class SPListInformation(ClientValue):

    def __init__(
        self,
        absolute_url: str = None,
        base_template: int = None,
        display_title: str = None,
        folder_info_list: ClientValueCollection[
            SPFolderInformation
        ] = ClientValueCollection(SPFolderInformation),
        id_: UUID = None,
        is_list_path_used_as_title: bool = None,
        is_my_site_document_library: bool = None,
        is_query_folders_throttled: bool = None,
        is_specified_or_default: bool = None,
        server_relative_url: str = None,
        show_warning: bool = None,
        title: str = None,
    ):
        self.AbsoluteUrl = absolute_url
        self.BaseTemplate = base_template
        self.DisplayTitle = display_title
        self.FolderInfoList = folder_info_list
        self.ID = id_
        self.IsListPathUsedAsTitle = is_list_path_used_as_title
        self.IsMySiteDocumentLibrary = is_my_site_document_library
        self.IsQueryFoldersThrottled = is_query_folders_throttled
        self.IsSpecifiedOrDefault = is_specified_or_default
        self.ServerRelativeUrl = server_relative_url
        self.ShowWarning = show_warning
        self.Title = title

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.SPListInformation"
