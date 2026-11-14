from __future__ import annotations

from datetime import time
from typing import TYPE_CHECKING, Optional

from typing_extensions import Self

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.queries.service_operation import ServiceOperationQuery
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata, version

if TYPE_CHECKING:
    from office365.common.microsoft_tunnel_configuration import MicrosoftTunnelConfiguration
    from office365.common.microsoft_tunnel_server import MicrosoftTunnelServer


@version("beta")
class MicrosoftTunnelSite(Entity):
    @odata(name="description")
    @property
    def description(self) -> Optional[str]:
        """Gets the description property"""
        return self.properties.get("description", None)

    @odata(name="displayName")
    @property
    def display_name(self) -> Optional[str]:
        """Gets the displayName property"""
        return self.properties.get("displayName", None)

    @odata(name="internalNetworkProbeUrl")
    @property
    def internal_network_probe_url(self) -> Optional[str]:
        """Gets the internalNetworkProbeUrl property"""
        return self.properties.get("internalNetworkProbeUrl", None)

    @odata(name="publicAddress")
    @property
    def public_address(self) -> Optional[str]:
        """Gets the publicAddress property"""
        return self.properties.get("publicAddress", None)

    @odata(name="roleScopeTagIds")
    @property
    def role_scope_tag_ids(self) -> StringCollection:
        """Gets the roleScopeTagIds property"""
        return self.properties.get("roleScopeTagIds", StringCollection())

    @odata(name="upgradeAutomatically")
    @property
    def upgrade_automatically(self) -> Optional[bool]:
        """Gets the upgradeAutomatically property"""
        return self.properties.get("upgradeAutomatically", None)

    @odata(name="upgradeAvailable")
    @property
    def upgrade_available(self) -> Optional[bool]:
        """Gets the upgradeAvailable property"""
        return self.properties.get("upgradeAvailable", None)

    @odata(name="upgradeWindowEndTime")
    @property
    def upgrade_window_end_time(self) -> Optional[time]:
        """Gets the upgradeWindowEndTime property"""
        return self.properties.get("upgradeWindowEndTime", None)

    @odata(name="upgradeWindowStartTime")
    @property
    def upgrade_window_start_time(self) -> Optional[time]:
        """Gets the upgradeWindowStartTime property"""
        return self.properties.get("upgradeWindowStartTime", None)

    @odata(name="upgradeWindowUtcOffsetInMinutes")
    @property
    def upgrade_window_utc_offset_in_minutes(self) -> Optional[int]:
        """Gets the upgradeWindowUtcOffsetInMinutes property"""
        return self.properties.get("upgradeWindowUtcOffsetInMinutes", None)

    @odata(name="microsoftTunnelConfiguration", navigation=True)
    @property
    def microsoft_tunnel_configuration(self) -> MicrosoftTunnelConfiguration:
        """Gets the microsoftTunnelConfiguration property"""
        from office365.common.microsoft_tunnel_configuration import MicrosoftTunnelConfiguration

        return self.properties.get(
            "microsoftTunnelConfiguration",
            MicrosoftTunnelConfiguration(self.context, ResourcePath("microsoftTunnelConfiguration", self.resource_path)),
        )

    @odata(name="microsoftTunnelServers", navigation=True)
    @property
    def microsoft_tunnel_servers(self) -> EntityCollection[MicrosoftTunnelServer]:
        """Gets the microsoftTunnelServers property"""
        from office365.common.microsoft_tunnel_server import MicrosoftTunnelServer

        return self.properties.get(
            "microsoftTunnelServers",
            EntityCollection[MicrosoftTunnelServer](
                self.context, MicrosoftTunnelServer, ResourcePath("microsoftTunnelServers", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.MicrosoftTunnelSite"

    def request_upgrade(self) -> Self:
        """requestUpgrade operation."""
        qry = ServiceOperationQuery(self, "requestUpgrade", None, {}, None, None)
        self.context.add_query(qry)
        return self
