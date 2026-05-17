from typing import Optional

from office365.runtime.client_value import ClientValue


class SPListModernUXOff(ClientValue):
    def __init__(
        self, is_hidden: Optional[bool] = None, is_read_only: Optional[bool] = None, value: Optional[bool] = None
    ):
        self.IsHidden = is_hidden
        self.IsReadOnly = is_read_only
        self.Value = value

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.SPListModernUXOff"
