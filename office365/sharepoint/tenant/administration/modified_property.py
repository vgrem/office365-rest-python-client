from typing import Optional

from office365.runtime.client_value import ClientValue


class ModifiedProperty(ClientValue):
    def __init__(
        self,
        name: Optional[str] = None,
        new_value: Optional[str] = None,
        old_value: Optional[str] = None,
        display_name: Optional[str] = None,
    ):
        self.Name = name
        self.NewValue = new_value
        self.OldValue = old_value
        self.displayName = display_name

    ""

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.SharePoint.Administration.TenantAdmin.ModifiedProperty"
