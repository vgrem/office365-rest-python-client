from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.copilot.package_detail import CopilotPackageDetail


class CopilotAdminCatalog(Entity):
    @odata(name="packages", navigation=True)
    @property
    def packages(self) -> EntityCollection[CopilotPackageDetail]:
        """Gets the packages property"""
        from office365.copilot.package_detail import CopilotPackageDetail

        return self.properties.get(
            "packages",
            EntityCollection[CopilotPackageDetail](
                self.context, CopilotPackageDetail, ResourcePath("packages", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.CopilotAdminCatalog"
