from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.planner.tasks.task import PlannerTask
from office365.runtime.paths.resource_path import ResourcePath

if TYPE_CHECKING:
    from office365.planner.plans.collection import PlannerPlanCollection


class PlannerUser(Entity):
    """The plannerUser resource provide access to Planner resources for a user.
    It doesn't contain any usable properties."""

    @property
    def plans(self) -> PlannerPlanCollection:
        """Returns the plannerTasks assigned to the user."""
        from office365.planner.plans.collection import PlannerPlanCollection

        return self.properties.get(
            "plans",
            PlannerPlanCollection(self.context, ResourcePath("plans", self.resource_path)),
        )

    @property
    def tasks(self) -> EntityCollection[PlannerTask]:
        """Returns the plannerTasks assigned to the user."""
        return self.properties.get(
            "tasks",
            EntityCollection(self.context, PlannerTask, ResourcePath("tasks", self.resource_path)),
        )
