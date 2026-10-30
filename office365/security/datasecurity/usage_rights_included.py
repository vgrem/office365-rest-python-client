from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.onedrive.sensitivitylabels.usagerights import UsageRights
from office365.runtime.types.odata_property import odata


class UsageRightsIncluded(Entity):
    @odata(name="ownerEmail")
    @property
    def owner_email(self) -> Optional[str]:
        """Gets the ownerEmail property"""
        return self.properties.get("ownerEmail", None)

    @odata(name="userEmail")
    @property
    def user_email(self) -> Optional[str]:
        """Gets the userEmail property"""
        return self.properties.get("userEmail", None)

    @odata(name="value")
    @property
    def value(self) -> UsageRights:
        """Gets the value property"""
        return self.properties.get("value", UsageRights.unknown)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UsageRightsIncluded"
