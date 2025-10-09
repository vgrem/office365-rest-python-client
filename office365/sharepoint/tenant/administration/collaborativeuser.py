from office365.runtime.client_value import ClientValue


class CollaborativeUser(ClientValue):

    def __init__(
        self,
        total_file_interaction: int = None,
        total_files_shared_externally: int = None,
        total_files_shared_internally: int = None,
        total_files_viewed_or_edited: int = None,
        user_principal_name: str = None,
    ):
        self.totalFileInteraction = total_file_interaction
        self.totalFilesSharedExternally = total_files_shared_externally
        self.totalFilesSharedInternally = total_files_shared_internally
        self.totalFilesViewedOrEdited = total_files_viewed_or_edited
        self.userPrincipalName = user_principal_name

    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Administration.TenantAdmin.CollaborativeUser"
