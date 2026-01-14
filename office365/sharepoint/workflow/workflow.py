from typing import Optional
from uuid import UUID

from office365.sharepoint.entity import Entity


class SPWorkflow(Entity):
    @property
    def association_id(self) -> Optional[UUID]:
        """Gets the AssociationId property"""
        return self.properties.get("AssociationId", None)

    @property
    def instance_id(self) -> Optional[UUID]:
        """Gets the InstanceId property"""
        return self.properties.get("InstanceId", None)

    @property
    def is_completed(self) -> Optional[bool]:
        """Gets the IsCompleted property"""
        return self.properties.get("IsCompleted", None)

    @property
    def status_text(self) -> Optional[str]:
        """Gets the StatusText property"""
        return self.properties.get("StatusText", None)

    @property
    def entity_type_name(self):
        return "SP.Workflow.SPWorkflow"
