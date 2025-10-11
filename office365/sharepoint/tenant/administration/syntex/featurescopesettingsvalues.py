from office365.runtime.client_value import ClientValue


class SyntexFeatureScopeSettingsValues(ClientValue):

    def __init__(self, enabled: bool = None, file_name: str = None):
        self.Enabled = enabled
        self.FileName = file_name

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.SyntexFeatureScopeSettingsValues"
