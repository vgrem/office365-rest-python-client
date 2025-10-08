from office365.runtime.client_value import ClientValue
from office365.sharepoint.copilot.files.user_relationship import (
    CopilotFileUserRelationship,
)
from office365.sharepoint.copilot.useridentity import UserIdentity


class CopilotFileMetadata(ClientValue):

    def __init__(
        self,
        container_url: str = None,
        created_by: UserIdentity = UserIdentity(),
        file_name: str = None,
        file_url: str = None,
        last_modified_by: UserIdentity = UserIdentity(),
        list_id: str = None,
        list_item_id: str = None,
        site_id: str = None,
        site_path: str = None,
        unique_id: str = None,
        user_relationship: CopilotFileUserRelationship = CopilotFileUserRelationship(),
        web_id: str = None,
    ):
        self.ContainerUrl = container_url
        self.CreatedBy = created_by
        self.FileName = file_name
        self.FileUrl = file_url
        self.LastModifiedBy = last_modified_by
        self.ListId = list_id
        self.ListItemId = list_item_id
        self.SiteId = site_id
        self.SitePath = site_path
        self.UniqueId = unique_id
        self.UserRelationship = user_relationship
        self.WebId = web_id

    " "

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Copilot.CopilotFileMetadata"
