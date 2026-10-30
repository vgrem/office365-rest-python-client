from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.admin.internet_explorer_mode import InternetExplorerMode


class Edge(Entity):
    @odata(name="internetExplorerMode", navigation=True)
    @property
    def internet_explorer_mode(self) -> InternetExplorerMode:
        """Gets the internetExplorerMode property"""
        from office365.admin.internet_explorer_mode import InternetExplorerMode

        return self.properties.get(
            "internetExplorerMode",
            InternetExplorerMode(self.context, ResourcePath("internetExplorerMode", self.resource_path)),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.Edge"
