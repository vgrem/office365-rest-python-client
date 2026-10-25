from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class FileSensitivityLabelInfo(Entity):
    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="LabelId")
    @property
    def label_id(self) -> Optional[str]:
        """Gets the LabelId property"""
        return self.properties.get("LabelId", None)

    @odata(name="ParentLabelId")
    @property
    def parent_label_id(self) -> Optional[str]:
        """Gets the ParentLabelId property"""
        return self.properties.get("ParentLabelId", None)

    @odata(name="ProtectionEnabled")
    @property
    def protection_enabled(self) -> Optional[bool]:
        """Gets the ProtectionEnabled property"""
        return self.properties.get("ProtectionEnabled", None)

    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantAdministration.FileSensitivityLabelInfo"
