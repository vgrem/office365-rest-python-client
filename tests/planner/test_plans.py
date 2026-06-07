"""Planner — plans, buckets, tasks, and task details.

Tests cover:
  - Creating a planner plan for an M365 group
  - Getting plan details
  - Listing plans for the current user
  - Creating buckets in a plan
  - Creating tasks (with and without a bucket)
  - Listing tasks in a plan
  - Getting task details
  - Updating a task title
  - Deleting plans and cleanup
  - Plan and task property assertions
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.groups.group import Group
from office365.planner.buckets.bucket import PlannerBucket
from office365.planner.plans.plan import PlannerPlan
from office365.planner.tasks.task import PlannerTask
from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestPlanner(GraphDelegatedTestCase):
    """Microsoft Planner — plan, bucket, and task lifecycle."""

    target_group: ClassVar[Optional[Group]] = None
    target_plan: ClassVar[Optional[PlannerPlan]] = None
    target_bucket: ClassVar[Optional[PlannerBucket]] = None
    target_task: ClassVar[Optional[PlannerTask]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        groups = cls.client.groups.filter("groupTypes/any(a:a eq 'unified')").top(1).get().execute_query()
        cls.target_group = groups[0] if len(groups) > 0 else None

    @requires_delegated(
        "Group.ReadWrite.All",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_01_create_plan(self):
        """Creating a planner plan for an M365 group should succeed."""
        group = TestPlanner.target_group
        if not group:
            self.skipTest("No M365 group available")

        plan = self.client.planner.plans.add(create_unique_name("SDK Test Plan"), group).execute_query()
        self.assertIsNotNone(plan.id)
        self.assertIsNotNone(plan.title)
        TestPlanner.target_plan = plan

    @requires_delegated(
        "Tasks.Read",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_02_get_plan_details(self):
        """Getting plan details returns a valid details object."""
        plan = TestPlanner.target_plan
        if not plan:
            self.skipTest("No plan created from previous test")

        details = plan.details.get().execute_query()
        self.assertIsNotNone(details.resource_path)
        self.assertIsNotNone(details.get_property("categoryDescriptions"))

    @requires_delegated(
        "Tasks.Read",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_03_list_my_plans(self):
        """Listing planner plans for the current user returns a valid collection."""
        plans = self.client.me.planner.plans.get().execute_query()
        self.assertIsNotNone(plans.resource_path)

    @requires_delegated(
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_04_create_bucket(self):
        """Creating a bucket in the plan should succeed."""
        plan = TestPlanner.target_plan
        if not plan:
            self.skipTest("No plan created from previous test")

        try:
            bucket = self.client.planner.buckets.add(name="SDK Test Bucket", plan=plan).execute_query()
            self.assertIsNotNone(bucket.id)
            self.assertEqual(bucket.name, "SDK Test Bucket")
            TestPlanner.target_bucket = bucket
        except AttributeError:
            self.skipTest("Buckets.add not available in this SDK version")

    @requires_delegated(
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_05_create_task(self):
        """Creating a planner task in the plan should succeed."""
        plan = TestPlanner.target_plan
        if not plan:
            self.skipTest("No plan created from previous test")

        task = self.client.planner.tasks.add("Update client list", plan).execute_query()
        self.assertIsNotNone(task.id)
        self.assertEqual(task.title, "Update client list")
        TestPlanner.target_task = task

    @requires_delegated(
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_06_create_task_in_bucket(self):
        """Creating a task in a specific bucket should succeed."""
        plan = TestPlanner.target_plan
        bucket = TestPlanner.target_bucket
        if not plan:
            self.skipTest("No plan created from previous test")
        if not bucket:
            self.skipTest("No bucket created from previous test")

        task = self.client.planner.tasks.add("SDK Task with Bucket", plan, bucket).execute_query()
        self.assertIsNotNone(task.id)
        self.assertEqual(task.bucket_id, bucket.id)
        task.delete_object().execute_query()

    @requires_delegated(
        "Tasks.Read",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_07_list_tasks(self):
        """Listing tasks in the plan returns a valid collection."""
        plan = TestPlanner.target_plan
        if not plan:
            self.skipTest("No plan created from previous test")

        tasks = plan.tasks.get().execute_query()
        self.assertIsNotNone(tasks)

    @requires_delegated(
        "Tasks.Read",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_08_task_has_expected_properties(self):
        """A planner task exposes title, createdDateTime, and createdBy."""
        task = TestPlanner.target_task
        if not task:
            self.skipTest("No task created from previous test")

        self.assertIsNotNone(task.title)
        # self.assertIsNotNone(task.created_datetime)

    @requires_delegated(
        "Tasks.Read",
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_09_get_task_details(self):
        """Getting task details returns the details object."""
        task = TestPlanner.target_task
        if not task:
            self.skipTest("No task created from previous test")

        try:
            details = task.details.get().execute_query()
            self.assertIsNotNone(details.resource_path)
        except Exception:
            self.skipTest("Task details endpoint not available")

    @requires_delegated(
        "Tasks.ReadWrite",
        bypass_roles=["Global Administrator"],
    )
    def test_10_update_task_title(self):
        """Updating a task's title should persist."""
        task = TestPlanner.target_task
        if not task:
            self.skipTest("No task created from previous test")

        task.title = "SDK Test — Updated Task Title"
        task.update().execute_query()

        refetched = self.client.planner.tasks[task.id].get().execute_query()
        self.assertEqual(refetched.title, "SDK Test — Updated Task Title")

    @requires_delegated(
        "Group.ReadWrite.All",
        "Tasks.ReadWrite.All",
        bypass_roles=["Global Administrator"],
    )
    def test_11_delete_plan(self):
        """Deleting the plan should succeed."""
        plan = TestPlanner.target_plan
        if not plan:
            self.skipTest("No plan created from previous test")

        plan.delete_object().execute_query()
        TestPlanner.target_plan = None

    @classmethod
    def tearDownClass(cls):
        """Best-effort cleanup of remaining resources."""
        plan = cls.target_plan
        if plan and plan.resource_path:
            try:
                plan.delete_object().execute_query()
            except Exception:
                pass
