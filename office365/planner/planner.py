from office365.entity import Entity
from office365.planner.buckets.collection import PlannerBucketCollection
from office365.planner.plans.collection import PlannerPlanCollection
from office365.planner.tasks.collection import PlannerTaskCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class Planner(Entity):
    """
    The planner resource is the entry point for the Planner object model.
    It returns a singleton planner resource. It doesn't contain any usable properties.
    """

    @odata(name="buckets", navigation=True)
    @property
    def buckets(self) -> PlannerBucketCollection:
        """Returns the plannerBuckets assigned to the user."""
        return self.properties.get(
            "buckets",
            PlannerBucketCollection(self.context),
        )

    @odata(name="tasks", navigation=True)
    @property
    def tasks(self) -> PlannerTaskCollection:
        """Returns the plannerTasks assigned to the user."""
        return self.properties.get(
            "tasks",
            PlannerTaskCollection(self.context),
        )

    @odata(name="plans", navigation=True)
    @property
    def plans(self) -> PlannerPlanCollection:
        """Returns the plannerTasks assigned to the user."""
        return self.properties.get(
            "plans",
            PlannerPlanCollection(self.context, ResourcePath("plans", self.resource_path)),
        )
