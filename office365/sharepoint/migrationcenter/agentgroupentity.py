from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from uuid import UUID

from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata
from office365.sharepoint.entity import Entity

if TYPE_CHECKING:
    from office365.sharepoint.migrationcenter.agentgroupentity import AgentGroupEntity


class AgentGroupEntity(Entity):
    @odata(name="Name")
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.AgentGroupEntity"

    @odata(name="Id")
    @property
    def id(self) -> Optional[UUID]:
        """Gets the Id property"""
        return self.properties.get("Id", None)

    @odata(name="Default", navigation=True)
    @property
    def default(self) -> AgentGroupEntity:
        """Gets the Default property"""
        from office365.sharepoint.migrationcenter.agentgroupentity import (
            AgentGroupEntity,
        )

        return self.properties.get(
            "Default", AgentGroupEntity(self.context, ResourcePath("Default", self.resource_path))
        )
