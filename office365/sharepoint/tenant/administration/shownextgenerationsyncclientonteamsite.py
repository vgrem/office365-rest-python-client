from office365.runtime.client_value import ClientValue
from typing import Optional


class ShowNextGenerationSyncClientOnTeamSite(ClientValue):
    def __init__(
        self,
        is_hidden: Optional[bool] = None,
        is_read_only: Optional[bool] = None,
        read_only_reason_code: Optional[int] = None,
        value: Optional[bool] = None,
    ):
        self.IsHidden = is_hidden
        self.IsReadOnly = is_read_only
        self.ReadOnlyReasonCode = read_only_reason_code
        self.Value = value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.ShowNextGenerationSyncClientOnTeamSite"
