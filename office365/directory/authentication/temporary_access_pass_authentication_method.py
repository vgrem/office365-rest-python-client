from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata


class TemporaryAccessPassAuthenticationMethod(Entity):
    @odata(name="isUsable")
    @property
    def is_usable(self) -> Optional[bool]:
        """Gets the isUsable property"""
        return self.properties.get("isUsable", None)

    @odata(name="isUsableOnce")
    @property
    def is_usable_once(self) -> Optional[bool]:
        """Gets the isUsableOnce property"""
        return self.properties.get("isUsableOnce", None)

    @odata(name="lifetimeInMinutes")
    @property
    def lifetime_in_minutes(self) -> Optional[int]:
        """Gets the lifetimeInMinutes property"""
        return self.properties.get("lifetimeInMinutes", None)

    @odata(name="methodUsabilityReason")
    @property
    def method_usability_reason(self) -> Optional[str]:
        """Gets the methodUsabilityReason property"""
        return self.properties.get("methodUsabilityReason", None)

    @odata(name="startDateTime")
    @property
    def start_date_time(self) -> Optional[datetime]:
        """Gets the startDateTime property"""
        return self.properties.get("startDateTime", datetime.min)

    @odata(name="temporaryAccessPass")
    @property
    def temporary_access_pass(self) -> Optional[str]:
        """Gets the temporaryAccessPass property"""
        return self.properties.get("temporaryAccessPass", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.TemporaryAccessPassAuthenticationMethod"
