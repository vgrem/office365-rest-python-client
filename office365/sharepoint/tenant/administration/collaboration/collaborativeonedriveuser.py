from typing import Optional

from office365.runtime.client_value import ClientValue


class CollaborativeOneDriveUser(ClientValue):
    def __init__(
        self,
        anonymous_link_count: Optional[int] = None,
        file_count: Optional[int] = None,
        files_shared_externally: Optional[int] = None,
        files_shared_internally: Optional[int] = None,
        total_files_shared: Optional[int] = None,
        user_principal_name: Optional[str] = None,
    ):
        self.anonymousLinkCount = anonymous_link_count
        self.fileCount = file_count
        self.filesSharedExternally = files_shared_externally
        self.filesSharedInternally = files_shared_internally
        self.totalFilesShared = total_files_shared
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeOneDriveUser"
