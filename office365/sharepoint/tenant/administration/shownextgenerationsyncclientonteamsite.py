from office365.runtime.client_value import ClientValue


class ShowNextGenerationSyncClientOnTeamSite(ClientValue):
    def __init__(
        self,
        is_hidden: bool = None,
        is_read_only: bool = None,
        read_only_reason_code: int = None,
        value: bool = None,
    ):
        self.IsHidden = is_hidden
        self.IsReadOnly = is_read_only
        self.ReadOnlyReasonCode = read_only_reason_code
        self.Value = value

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.TenantAdministration.ShowNextGenerationSyncClientOnTeamSite"
