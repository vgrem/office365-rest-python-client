from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class UserExperienceAnalyticsDeviceScope(Entity):
    @odata(name="createdDateTime")
    @property
    def created_date_time(self) -> Optional[datetime]:
        """Gets the createdDateTime property"""
        return self.properties.get("createdDateTime", None)

    @odata(name="deviceScopeName")
    @property
    def device_scope_name(self) -> Optional[str]:
        """Gets the deviceScopeName property"""
        return self.properties.get("deviceScopeName", None)

    @odata(name="enabled")
    @property
    def enabled(self) -> Optional[bool]:
        """Gets the enabled property"""
        return self.properties.get("enabled", None)

    @odata(name="isBuiltIn")
    @property
    def is_built_in(self) -> Optional[bool]:
        """Gets the isBuiltIn property"""
        return self.properties.get("isBuiltIn", None)

    @odata(name="lastModifiedDateTime")
    @property
    def last_modified_date_time(self) -> Optional[datetime]:
        """Gets the lastModifiedDateTime property"""
        return self.properties.get("lastModifiedDateTime", None)

    @odata(name="ownerId")
    @property
    def owner_id(self) -> Optional[str]:
        """Gets the ownerId property"""
        return self.properties.get("ownerId", None)

    @odata(name="value")
    @property
    def value(self) -> Optional[str]:
        """Gets the value property"""
        return self.properties.get("value", None)

    @odata(name="valueObjectId")
    @property
    def value_object_id(self) -> Optional[str]:
        """Gets the valueObjectId property"""
        return self.properties.get("valueObjectId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.UserExperienceAnalyticsDeviceScope"
