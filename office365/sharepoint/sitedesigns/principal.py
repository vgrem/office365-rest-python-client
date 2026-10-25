from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class SiteDesignPrincipal(Entity):
    @property
    def entity_type_name(self):
        return "Microsoft.SharePoint.Utilities.WebTemplateExtensions.SiteDesignPrincipal"

    @odata(name="DisplayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the DisplayName property"""
        return self.properties.get("DisplayName", None)

    @odata(name="PrincipalName")
    @property
    def principal_name(self) -> Optional[str]:
        """Gets the PrincipalName property"""
        return self.properties.get("PrincipalName", None)

    @odata(name="Rights")
    @property
    def rights(self) -> Optional[int]:
        """Gets the Rights property"""
        return self.properties.get("Rights", None)
