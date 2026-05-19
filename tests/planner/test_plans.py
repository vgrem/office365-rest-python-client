"""Tests for Microsoft Planner API."""

from typing import Optional

from office365.directory.groups.group import Group
from office365.planner.plans.plan import PlannerPlan
from tests import create_unique_name
from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestPlanner(GraphDelegatedTestCase):
    """Tests for Microsoft Planner API."""

    target_group: Optional[Group] = None
    target_plan: Optional[PlannerPlan] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        groups = cls.client.groups.filter("groupTypes/any(a:a eq 'unified')").get().execute_query()
        cls.target_group = groups[0]

    @requires_delegated_permission_or_role(
        "Group.ReadWrite.All",
        "Tasks.ReadWrite",
        roles=["Global Administrator"],
    )
    def test1_create_plan(self):
        """Create a planner plan for a group."""
        plan_name = create_unique_name("My Plan")
        assert TestPlanner.target_group is not None
        new_plan = self.client.planner.plans.add(plan_name, TestPlanner.target_group).execute_query()
        self.assertIsNotNone(new_plan.id)
        TestPlanner.target_plan = new_plan

    @requires_delegated_permission_or_role(
        "Tasks.Read",
        "Tasks.ReadWrite",
        roles=["Global Administrator"],
    )
    def test2_get_plan_details(self):
        """Get the details of a planner plan."""
        plan = TestPlanner.target_plan
        assert plan is not None
        result = plan.details.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role(
        "Tasks.Read",
        "Tasks.ReadWrite",
        roles=["Global Administrator"],
    )
    def test3_list_my_plans(self):
        """List planner plans for the current user."""
        my_plans = self.client.me.planner.plans.get().execute_query()
        self.assertIsNotNone(my_plans.resource_path)
        self.assertGreaterEqual(len(my_plans), 0)

    @requires_delegated_permission_or_role(
        "Tasks.ReadWrite",
        roles=["Global Administrator"],
    )
    def test4_create_task(self):
        """Create a planner task within the plan."""
        plan = TestPlanner.target_plan
        assert plan is not None
        task = self.client.planner.tasks.add("Update client list", plan).execute_query()
        self.assertIsNotNone(task.resource_path)

    @requires_delegated_permission_or_role(
        "Tasks.Read",
        "Tasks.ReadWrite",
        roles=["Global Administrator"],
    )
    def test5_list_tasks(self):
        """List all tasks in the planner plan."""
        plan = TestPlanner.target_plan
        assert plan is not None
        tasks = plan.tasks.get().execute_query()
        self.assertGreaterEqual(len(tasks), 0)

    @requires_delegated_permission_or_role(
        "Group.ReadWrite.All",
        "Tasks.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test6_delete_plan(self):
        """Delete the planner plan and clean up."""
        plan = TestPlanner.target_plan
        assert plan is not None
        plan.delete_object().execute_query()
        TestPlanner.target_plan = None
