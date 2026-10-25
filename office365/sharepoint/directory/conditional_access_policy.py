from __future__ import annotations

from typing import Optional

from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity


class ConditionalAccessPolicy(Entity):
    @odata(name="conditions")
    @property
    def conditions(self) -> Optional[str]:
        """Gets the conditions property"""
        return self.properties.get("conditions", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="grantControls")
    @property
    def grant_controls(self) -> Optional[str]:
        """Gets the grantControls property"""
        return self.properties.get("grantControls", None)

    @odata(name="id")
    @property
    def id_(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @odata(name="sessionControls")
    @property
    def session_controls(self) -> Optional[str]:
        """Gets the sessionControls property"""
        return self.properties.get("sessionControls", None)

    @odata(name="state")
    @property
    def state(self) -> Optional[str]:
        """Gets the state property"""
        return self.properties.get("state", None)

    @odata(name="templateId")
    @property
    def template_id(self) -> Optional[str]:
        """Gets the templateId property"""
        return self.properties.get("templateId", None)

    @property
    def entity_type_name(self) -> str:
        return "SP.Directory.ConditionalAccessPolicy"

    @odata(name="id")
    @property
    def id(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)
