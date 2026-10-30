from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.collections import StringCollection
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.communications.calls.routingmode import RoutingMode


class AudioRoutingGroup(Entity):
    @odata(name="receivers")
    @property
    def receivers(self) -> StringCollection:
        """Gets the receivers property"""
        return self.properties.get("receivers", StringCollection())

    @odata(name="routingMode")
    @property
    def routing_mode(self) -> RoutingMode:
        """Gets the routingMode property"""
        from office365.communications.calls.routingmode import RoutingMode

        return self.properties.get("routingMode", RoutingMode.oneToOne)

    @odata(name="sources")
    @property
    def sources(self) -> StringCollection:
        """Gets the sources property"""
        return self.properties.get("sources", StringCollection())

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.AudioRoutingGroup"
