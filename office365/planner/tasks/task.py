from datetime import datetime
from typing import Optional

from typing_extensions import Self

from office365.directory.permissions.identity_set import IdentitySet
from office365.entity import Entity
from office365.planner.assignments import PlannerAssignments
from office365.planner.tasks.task_details import PlannerTaskDetails
from office365.runtime.http.request_options import RequestOptions
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class PlannerTask(Entity):
    """
    The plannerTask resource represents a Planner task in Microsoft 365.
    A Planner task is contained in a plan and can be assigned to a bucket in a plan.
    Each task object has a details object which can contain more information about the task.
    See overview for more information regarding relationships between group, plan and task.
    """

    def delete_object(self) -> Self:
        def _construct_request(request: RequestOptions) -> None:
            etag = self.properties.get("__etag")
            if etag:
                request.set_header("If-Match", etag)

        super().delete_object().before_execute(_construct_request)
        return self

    def update(self) -> Self:
        def _construct_request(request: RequestOptions) -> None:
            etag = self.properties.get("__etag")
            if etag:
                request.set_header("If-Match", etag)

        super().update().before_execute(_construct_request)
        return self

    @odata(name="createdBy")
    @property
    def created_by(self) -> IdentitySet:
        """Identity of the user that created the task."""
        return self.properties.get("createdBy", IdentitySet())

    @odata(name="createdDateTime")
    @property
    def created_datetime(self) -> datetime:
        """
        Date and time at which the task is created.
        """
        return self.properties.get("createdDateTime", datetime.min)

    @property
    def title(self) -> Optional[str]:
        """Required. Title of the task."""
        return self.properties.get("title", None)

    @title.setter
    def title(self, value):
        self.set_property("title", value)

    @property
    def plan_id(self) -> Optional[str]:
        """Required. Name of the bucket."""
        return self.properties.get("planId", None)

    @plan_id.setter
    def plan_id(self, value: str):
        self.set_property("planId", value)

    @property
    def bucket_id(self) -> Optional[str]:
        """Required. Name of the bucket."""
        return self.properties.get("bucketId", None)

    @bucket_id.setter
    def bucket_id(self, value: str):
        self.set_property("bucketId", value)

    @property
    def details(self) -> PlannerTaskDetails:
        """Additional details about the task."""
        return self.properties.get(
            "details",
            PlannerTaskDetails(self.context, ResourcePath("details", self.resource_path)),
        )

    @property
    def percent_complete(self) -> int:
        """Percentage of task completion. 0 = not started, 100 = complete."""
        return self.properties.get("percentComplete", 0)

    @property
    def priority(self) -> int:
        """Priority of the task. 0 = urgent, ..., 5 = medium, 10 = low."""
        return self.properties.get("priority", 5)

    @property
    def assignments(self) -> PlannerAssignments:
        """The set of users assigned to this task (keyed by user ID)."""
        return self.properties.get("assignments", PlannerAssignments())
