from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MicrosoftTunnelHealthThreshold(Entity):
    @odata(name="defaultHealthyThreshold")
    @property
    def default_healthy_threshold(self) -> Optional[int]:
        """Gets the defaultHealthyThreshold property"""
        return self.properties.get("defaultHealthyThreshold", None)

    @odata(name="defaultUnhealthyThreshold")
    @property
    def default_unhealthy_threshold(self) -> Optional[int]:
        """Gets the defaultUnhealthyThreshold property"""
        return self.properties.get("defaultUnhealthyThreshold", None)

    @odata(name="healthyThreshold")
    @property
    def healthy_threshold(self) -> Optional[int]:
        """Gets the healthyThreshold property"""
        return self.properties.get("healthyThreshold", None)

    @odata(name="unhealthyThreshold")
    @property
    def unhealthy_threshold(self) -> Optional[int]:
        """Gets the unhealthyThreshold property"""
        return self.properties.get("unhealthyThreshold", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelHealthThreshold"
