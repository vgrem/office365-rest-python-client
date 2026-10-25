from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ThemeProperties(Entity):
    @property
    def entity_type_name(self):  # type: ignore[override]
        return "Microsoft.Online.SharePoint.TenantManagement.ThemeProperties"

    @odata(name="ColorPairsJson")
    @property
    def color_pairs_json(self) -> Optional[str]:
        """Gets the ColorPairsJson property"""
        return self.properties.get("ColorPairsJson", None)

    @odata(name="Editable")
    @property
    def editable(self) -> Optional[bool]:
        """Gets the Editable property"""
        return self.properties.get("Editable", None)

    @odata(name="IsInverted")
    @property
    def is_inverted(self) -> Optional[bool]:
        """Gets the IsInverted property"""
        return self.properties.get("IsInverted", None)

    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)
