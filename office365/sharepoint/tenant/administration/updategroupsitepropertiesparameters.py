from office365.runtime.client_value import ClientValue


class UpdateGroupSitePropertiesParameters(ClientValue):

    def __init__(
        self, storage_maximum_level: int = None, storage_warning_level: int = None
    ):
        self.storageMaximumLevel = storage_maximum_level
        self.storageWarningLevel = storage_warning_level

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.UpdateGroupSitePropertiesParameters"
