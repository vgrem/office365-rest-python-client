from __future__ import annotations

from office365.runtime.paths.resource_path import ResourcePath
from office365.sharepoint.entity import Entity


class WorkflowSubscriptionService(Entity):
    @property
    def current(self) -> WorkflowSubscriptionService:
        """Gets the Current property"""
        return self.properties.get(
            "Current", WorkflowSubscriptionService(self.context, ResourcePath("Current", self.resource_path))
        )

    @property
    def entity_type_name(self):
        return "SP.WorkflowServices.WorkflowSubscriptionService"
