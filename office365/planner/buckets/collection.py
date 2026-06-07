from __future__ import annotations

from office365.entity_collection import EntityCollection
from office365.planner.buckets.bucket import PlannerBucket
from office365.planner.plans.plan import PlannerPlan
from office365.runtime.queries.create_entity import CreateEntityQuery


class PlannerBucketCollection(EntityCollection[PlannerBucket]):
    def __init__(self, context, resource_path=None):
        super().__init__(context, PlannerBucket, resource_path)

    def add(
        self,
        name: str,
        plan: str | PlannerPlan,
    ) -> PlannerBucket:
        """ """
        return_type = PlannerBucket(self.context)
        self.add_child(return_type)
        return_type.name = name

        def _add(plan_id: str | None) -> None:
            assert plan_id is not None
            return_type.plan_id = plan_id
            qry = CreateEntityQuery(self, return_type, return_type)
            self.context.add_query(qry)

        if isinstance(plan, PlannerPlan):
            plan.ensure_property("id").after_execute(lambda _: _add(plan.id))
        else:
            _add(plan)

        return return_type
