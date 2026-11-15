from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.entity import Entity
from office365.intune.devices.management.microsoft_tunnel_deployment_mode import MicrosoftTunnelDeploymentMode
from office365.intune.devices.management.microsoft_tunnel_server_health_status import MicrosoftTunnelServerHealthStatus
from office365.runtime.types.odata_property import odata, version


@version("beta")
class MicrosoftTunnelServer(Entity):
    @odata(name="agentImageDigest")
    @property
    def agent_image_digest(self) -> Optional[str]:
        """Gets the agentImageDigest property"""
        return self.properties.get("agentImageDigest", None)

    @odata(name="deploymentMode")
    @property
    def deployment_mode(self) -> Optional[MicrosoftTunnelDeploymentMode]:
        """Gets the deploymentMode property"""
        return self.properties.get("deploymentMode", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="lastCheckinDateTime")
    @property
    def last_checkin_date_time(self) -> Optional[datetime]:
        """Gets the lastCheckinDateTime property"""
        return self.properties.get("lastCheckinDateTime", None)

    @odata(name="serverImageDigest")
    @property
    def server_image_digest(self) -> Optional[str]:
        """Gets the serverImageDigest property"""
        return self.properties.get("serverImageDigest", None)

    @odata(name="tunnelServerHealthStatus")
    @property
    def tunnel_server_health_status(self) -> Optional[MicrosoftTunnelServerHealthStatus]:
        """Gets the tunnelServerHealthStatus property"""
        return self.properties.get("tunnelServerHealthStatus", None)

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelServer"
