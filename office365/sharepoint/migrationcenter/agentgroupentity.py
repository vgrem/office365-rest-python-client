from typing import Optional

from office365.sharepoint.entity import Entity


class AgentGroupEntity(Entity):
    @property
    def name(self) -> Optional[str]:
        """Gets the Name property"""
        return self.properties.get("Name", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Common.AgentGroupEntity"
