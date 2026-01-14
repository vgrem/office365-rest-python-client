from office365.runtime.client_value import ClientValue


class CollaborativeOneDriveUser(ClientValue):
    def __init__(
        self,
        anonymous_link_count: int = None,
        file_count: int = None,
        files_shared_externally: int = None,
        files_shared_internally: int = None,
        total_files_shared: int = None,
        user_principal_name: str = None,
    ):
        self.anonymousLinkCount = anonymous_link_count
        self.fileCount = file_count
        self.filesSharedExternally = files_shared_externally
        self.filesSharedInternally = files_shared_internally
        self.totalFilesShared = total_files_shared
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeOneDriveUser"
