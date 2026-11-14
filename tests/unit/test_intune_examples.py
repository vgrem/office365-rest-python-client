"""The two Intune example helpers that state a contract rather than call a tenant.

``backup.document`` is the shape a backup file has to keep, and ``assignments.describe`` is
what turns an assignment target into a sentence. Both are pure, so they are pinned here; the
examples themselves are verified against a tenant by running them.
"""

import importlib.util
from pathlib import Path
from types import SimpleNamespace
from unittest import TestCase

from office365.directory.policies.conditionalaccess.device_and_app_management_assignment_target import (
    DeviceAndAppManagementAssignmentTarget,
)

EXAMPLES = Path(__file__).resolve().parents[2] / "examples" / "intune" / "policies"


def load(name: str):
    spec = importlib.util.spec_from_file_location(name, EXAMPLES / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class TestPolicyBackup(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.backup = load("backup")

    def test_a_file_keeps_the_name_and_the_id(self):
        policy = SimpleNamespace(display_name="Wi-Fi / Corp", id="abc-123")
        self.assertEqual(self.backup.file_name(policy), "wi-fi-corp-abc-123.json")

    def test_a_document_carries_the_policy_and_its_targets(self):
        policy = SimpleNamespace(
            entity_type_name="microsoft.graph.DeviceConfiguration",
            id="abc-123",
            display_name="Wi-Fi / Corp",
            to_json=lambda: {"displayName": "Wi-Fi / Corp"},
        )
        assignment = SimpleNamespace(to_json=lambda: {"target": {"groupId": "g-1"}})
        document = self.backup.document(policy, [assignment])
        self.assertEqual(document["@odata.type"], "microsoft.graph.DeviceConfiguration")
        self.assertEqual(document["policy"], {"displayName": "Wi-Fi / Corp"})
        self.assertEqual(document["assignments"], [{"target": {"groupId": "g-1"}}])


class TestAssignmentTarget(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.assignments = load("assignments")

    def test_a_group_target_is_named(self):
        target = DeviceAndAppManagementAssignmentTarget(group_id="g-1")
        self.assertEqual(self.assignments.describe(target, {"g-1": "All Windows"}), "group All Windows")

    def test_an_unresolved_group_stays_an_id(self):
        target = DeviceAndAppManagementAssignmentTarget(group_id="g-1")
        self.assertEqual(self.assignments.describe(target, {}), "group g-1")

    def test_a_filtered_target_says_so(self):
        target = DeviceAndAppManagementAssignmentTarget(
            group_id="g-1", device_and_app_management_assignment_filter_id="f-1"
        )
        self.assertEqual(self.assignments.describe(target, {"g-1": "All Windows"}), "group All Windows (filter f-1)")

    def test_a_target_without_a_group_reaches_everything(self):
        any_target = DeviceAndAppManagementAssignmentTarget()
        self.assertEqual(self.assignments.describe(any_target, {}), "all devices and users")
