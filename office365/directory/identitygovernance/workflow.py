from __future__ import annotations

from datetime import datetime
from typing import Optional

from office365.directory.identitygovernance.workflow_version import WorkflowVersion
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath


class Workflow(Entity):
    @property
    def deleted_date_time(self) -> datetime:
        """Gets the deletedDateTime property"""
        return self.properties.get("deletedDateTime", datetime.min)

    @property
    def id_(self) -> Optional[str]:
        """Gets the id property"""
        return self.properties.get("id", None)

    @property
    def next_schedule_run_date_time(self) -> datetime:
        """Gets the nextScheduleRunDateTime property"""
        return self.properties.get("nextScheduleRunDateTime", datetime.min)

    @property
    def version(self) -> Optional[int]:
        """Gets the version property"""
        return self.properties.get("version", None)

    @property
    def versions(self) -> EntityCollection[WorkflowVersion]:
        """Gets the versions property"""
        return self.properties.get(
            "versions",
            EntityCollection[WorkflowVersion](
                self.context, WorkflowVersion, ResourcePath("versions", self.resource_path)
            ),
        )

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.identityGovernance.Workflow"
