from typing import Optional

from office365.runtime.types.collections import GuidCollection
from office365.sharepoint.entity import Entity


class AgentGroup(Entity):

    @property
    def active_agent_count(self) -> Optional[int]:
        """Gets the ActiveAgentCount property"""
        return self.properties.get("ActiveAgentCount", None)

    @property
    def active_agent_id_list(self) -> GuidCollection:
        """Gets the ActiveAgentIdList property"""
        return self.properties.get("ActiveAgentIdList", GuidCollection())

    @property
    def agent_count(self) -> Optional[int]:
        """Gets the AgentCount property"""
        return self.properties.get("AgentCount", None)

    @property
    def agent_id_list(self) -> GuidCollection:
        """Gets the AgentIdList property"""
        return self.properties.get("AgentIdList", GuidCollection())

    @property
    def task_count(self) -> Optional[int]:
        """Gets the TaskCount property"""
        return self.properties.get("TaskCount", None)

    @property
    def entity_type_name(self):
        return "Microsoft.Online.SharePoint.MigrationCenter.Service.AgentGroup"
