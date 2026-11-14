from __future__ import annotations

from typing import Optional

from office365.entity import Entity
from office365.runtime.types.odata_property import odata, version


@version("beta")
class WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary(Entity):
    @odata(name="deployedDeviceCount")
    @property
    def deployed_device_count(self) -> Optional[int]:
        """Gets the deployedDeviceCount property"""
        return self.properties.get("deployedDeviceCount", None)

    @odata(name="failedDeviceCount")
    @property
    def failed_device_count(self) -> Optional[int]:
        """Gets the failedDeviceCount property"""
        return self.properties.get("failedDeviceCount", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.WindowsDefenderApplicationControlSupplementalPolicyDeploymentSummary"
