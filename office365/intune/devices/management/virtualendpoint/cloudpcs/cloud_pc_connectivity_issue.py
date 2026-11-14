from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class CloudPCConnectivityIssue(Entity):
    @odata(name="deviceId")
    @property
    def device_id(self) -> Optional[str]:
        """Gets the deviceId property"""
        return self.properties.get("deviceId", None)

    @odata(name="errorCode")
    @property
    def error_code(self) -> Optional[str]:
        """Gets the errorCode property"""
        return self.properties.get("errorCode", None)

    @odata(name="errorDateTime")
    @property
    def error_date_time(self) -> Optional[datetime]:
        """Gets the errorDateTime property"""
        return self.properties.get("errorDateTime", None)

    @odata(name="errorDescription")
    @property
    def error_description(self) -> Optional[str]:
        """Gets the errorDescription property"""
        return self.properties.get("errorDescription", None)

    @odata(name="recommendedAction")
    @property
    def recommended_action(self) -> Optional[str]:
        """Gets the recommendedAction property"""
        return self.properties.get("recommendedAction", None)

    @odata(name="userId")
    @property
    def user_id(self) -> Optional[str]:
        """Gets the userId property"""
        return self.properties.get("userId", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CloudPCConnectivityIssue"
