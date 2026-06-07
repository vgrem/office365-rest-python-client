from __future__ import annotations

from typing import Union

from office365.entity_collection import EntityCollection
from office365.planner.buckets.bucket import PlannerBucket
from office365.planner.plans.plan import PlannerPlan
from office365.planner.tasks.task import PlannerTask
from office365.runtime.queries.create_entity import CreateEntityQuery


class PlannerTaskCollection(EntityCollection[PlannerTask]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, PlannerTask, resource_path)

    def add(
        self,
        title: str,
        plan: Union[str, PlannerPlan],
        bucket: str | PlannerBucket | None = None,
    ) -> PlannerTask:
        """
        Create a new plannerTask.

        :param str title: Task title
        :param str|PlannerPlan plan: Plan identifier or Plan object
        :param str|PlannerBucket bucket: Bucket identifier or Plan object
        """
        return_type = PlannerTask(self.context)
        self.add_child(return_type)
        return_type.title = title

        def _add(plan_id: str | None, bucket_id: str | None) -> None:
            assert plan_id is not None
            # payload = {"title": title, "planId": plan_id, "bucket_id": bucket_id}
            return_type.plan_id = plan_id
            qry = CreateEntityQuery(self, return_type, return_type)
            self.context.add_query(qry)

        def _ensure_bucket():
            if isinstance(bucket, PlannerBucket):
                bid: str | None = bucket.id
                bucket.ensure_property("id").after_execute(lambda _: _ensure_plan(bid))
            else:
                _ensure_plan(bucket)

        def _ensure_plan(bucket_id: str | None) -> None:
            if bucket_id:
                return_type.bucket_id = bucket_id
            if isinstance(plan, PlannerPlan):
                pid: str | None = plan.id
                plan.ensure_property("id").after_execute(lambda _: _add(pid, bucket_id))
            else:
                _add(plan, bucket_id)

        if bucket is not None:
            _ensure_bucket()
        else:
            _ensure_plan(None)

        return return_type
