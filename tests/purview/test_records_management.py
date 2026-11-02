"""Retention labels, records management, and file plan descriptors.

Two measured tenant facts shape this suite, and both are skips rather than failures:

- **The retention feeds refuse every standard query option.** ``$filter``, ``$top``,
  ``$skip``, ``$orderby`` and ``$select`` all answer ``400 ... Query option 'Filter' is
  not allowed``, so the client refuses them before the request
  (``@query_capabilities`` on the two collections). Anything that needs a subset is
  bounded here, and there is no pagination test to write: the server has no page size.
- **Both feeds are gated by Purview's own RBAC, not by the Entra role or the
  ``RecordsManagement.*`` scope.** A bare ``GET`` answers ``500 DataInsights
  command(GET) FAILED - Forbidden`` for a user holding Compliance Administrator, and it
  answers it *intermittently*: the same call succeeds, then names the mailbox server that
  refused it (``TargetServer = BESPR09MB...eurprd09.prod.outlook.com``). No client change
  can fix that, so :meth:`_RetentionTestCase.purview` skips on it.

The tests still cover the label lifecycle - create, read back by id, inspect, reject an
empty name and a zero duration - so a tenant whose user *is* covered by Purview RBAC
gets the whole suite.
"""

from __future__ import annotations

from typing import ClassVar, Optional
from uuid import uuid4

from office365.permissions import DirectoryRole
from office365.runtime.client_request_exception import ClientRequestException
from office365.security.labels.retention.actionafterretentionperiod import (
    ActionAfterRetentionPeriod,
)
from office365.security.labels.retention.behaviorduringretentionperiod import (
    BehaviorDuringRetentionPeriod,
)
from office365.security.labels.retention.collection import RetentionLabelCollection
from office365.security.labels.retention.defaultrecordbehavior import (
    DefaultRecordBehavior,
)
from office365.security.labels.retention.duration_in_days import (
    RetentionDurationInDays,
)
from office365.security.labels.retention.label import RetentionLabel
from office365.security.labels.retention.trigger import RetentionTrigger

from tests.decorators import requires_call, requires_delegated
from tests.graph_case import GraphDelegatedTestCase

# Common permission set for records management operations
_RM_READ = ("RecordsManagement.Read.All", "RecordsManagement.ReadWrite.All")
_RM_WRITE = ("RecordsManagement.ReadWrite.All",)
# Entra publishes both of these as role templates. "Records Management" is not one: it is a
# Purview portal role with no directory template, so it can be neither assigned through the
# directory nor read back from it - naming it made the grant plan name an operation that
# cannot succeed.
_RM_ROLES = [
    DirectoryRole.ComplianceAdministrator,
    DirectoryRole.ComplianceDataAdministrator,
]
# The capability, not the packaging: Records Management is a service plan, and the retail E5
# SKUs are only the way it is usually bought. A tenant whose seats come from an E5 developer
# pack carries the same plan, and naming the SKUs alone skipped these tests for a user who
# could make every call.
_RM_LICENSES = ["RECORDS_MANAGEMENT"]

#: How the Purview gate names itself, and the status it refuses with. Keyed on the wording and
#: not on ``500``: the retention cmdlets answer 500 for *every* failure, including the
#: validation errors the negative tests below expect ("displayName can not be empty"), so a
#: status-only gate would turn two passing assertions into skips.
_PURVIEW_REFUSAL = ("DataInsights command", "TargetServer")
_PURVIEW_STATUSES = frozenset({403})


class _RetentionTestCase(GraphDelegatedTestCase):
    """A Purview RBAC refusal is a fact about the tenant, so it skips instead of failing."""

    def purview(self, call):
        """Run ``call``; when Purview's own RBAC refuses it, skip this test rather than fail."""
        try:
            return call()
        except ClientRequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            if status in _PURVIEW_STATUSES or any(marker in str(exc) for marker in _PURVIEW_REFUSAL):
                self.skipTest(f"Purview RBAC does not cover this user ({status}): {exc}")
            raise

    def read(self, resource):
        """Read ``resource`` and hand back the loaded object, the way the suite reads any one."""
        return self.purview(lambda: resource.get().execute_query())


class TestRetentionEventTypes(_RetentionTestCase):
    """Event types are used to trigger retention when an event of that type occurs."""

    @requires_delegated(
        *_RM_READ,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_01_list_retention_event_types(self):
        """Retrieving all retention event types returns a collection with a valid path."""
        result = self.read(self.client.security.trigger_types.retention_event_types)
        self.assertIsNotNone(result.resource_path)
        self.assertIsNotNone(result.context)


class TestRetentionLabels(_RetentionTestCase):
    """Retention labels - the core of Purview Records Management."""

    created_label: ClassVar[Optional[RetentionLabel]] = None

    @requires_delegated(
        *_RM_READ,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_01_list_labels_empty_result_graceful(self):
        """Listing retention labels when none exist returns a valid collection (not None)."""
        result = self.read(self.client.security.labels.retention_labels)
        self.assertIsNotNone(result.resource_path)

    @requires_call(
        RetentionLabelCollection.add,
        flow="delegated",
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_02_create_retention_label_full(self):
        """Creating a full retention label with 365-day retention, record behavior, and delete action."""
        # Display names are unique per tenant and the server refuses a duplicate, so the name
        # carries a nonce: a run that dies before its teardown must not poison the next one.
        label_name = f"SDK_TEST_Retain1Year_{uuid4().hex[:12]}"
        result = self.purview(
            lambda: self.client.security.labels.retention_labels.add(
                label_name,
                RetentionTrigger.dateLabeled,
                RetentionDurationInDays(365),
                BehaviorDuringRetentionPeriod.retainAsRecord,
                DefaultRecordBehavior.startLocked,
                ActionAfterRetentionPeriod.delete,
            ).execute_query()
        )
        # Assigned before the assertions so a failed one still leaves the label to the
        # teardown: the create is the expensive half and it has already happened.
        TestRetentionLabels.created_label = result
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), label_name)
        # The wire form is the member *name*, so the round trip is an enum member and not the
        # string "dateLabeled"; comparing to the string asserted the payload spelling instead.
        self.assertEqual(result.get_property("retentionTrigger"), RetentionTrigger.dateLabeled)

    @requires_delegated(
        *_RM_READ,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_03_get_label_by_id(self):
        """Retrieving a retention label by its ID returns the expected label."""
        created = self._created()
        result = self.read(self.client.security.labels.retention_labels[created.id])
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("id"), created.id)
        self.assertEqual(result.get_property("displayName"), created.get_property("displayName"))

    @requires_delegated(
        *_RM_READ,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_04_label_has_expected_properties(self):
        """A retention label exposes retentionTrigger, behaviorDuringRetentionPeriod, etc."""
        created = self._created()
        label = self.read(self.client.security.labels.retention_labels[created.id])
        self.assertIsNotNone(label.get_property("retentionTrigger"))
        self.assertIsNotNone(label.get_property("behaviorDuringRetentionPeriod"))
        self.assertIsNotNone(label.get_property("actionAfterRetentionPeriod"))

    def _created(self) -> RetentionLabel:
        """The label the create test made, or a skip naming why there is none."""
        created = TestRetentionLabels.created_label
        if not created:
            self.skipTest("No created label available from previous test")
        return created

    @classmethod
    def tearDownClass(cls):
        """Clean up the created retention label if one exists."""
        label = cls.created_label
        if label and label.resource_path:
            try:
                label.delete_object().execute_query()
            except Exception:
                pass  # Best-effort cleanup


class TestRetentionLabelNegativeCases(_RetentionTestCase):
    """Verify expected failures and edge cases for retention labels."""

    @requires_delegated(
        *_RM_WRITE,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_01_empty_display_name_rejected(self):
        """Creating a label with an empty display name should raise an error."""

        def create():
            return self.client.security.labels.retention_labels.add(
                "",
                RetentionTrigger.dateLabeled,
                RetentionDurationInDays(1),
                BehaviorDuringRetentionPeriod.retainAsRecord,
                DefaultRecordBehavior.startLocked,
                ActionAfterRetentionPeriod.delete,
            ).execute_query()

        with self.assertRaises(ClientRequestException):
            self.purview(create)

    @requires_delegated(
        *_RM_WRITE,
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_02_zero_duration_rejected(self):
        """Creating a label with zero retention days should be rejected by the API."""

        def create():
            return self.client.security.labels.retention_labels.add(
                "SDK_TEST_ZeroDays",
                RetentionTrigger.dateLabeled,
                RetentionDurationInDays(0),
                BehaviorDuringRetentionPeriod.retainAsRecord,
                DefaultRecordBehavior.startLocked,
                ActionAfterRetentionPeriod.delete,
            ).execute_query()

        with self.assertRaises(ClientRequestException):
            self.purview(create)


class TestRetentionLabelFilePlan(_RetentionTestCase):
    """File plan descriptors enrich retention labels with business context."""

    @requires_delegated(
        "RecordsManagement.Read.All",
        require_roles=_RM_ROLES,
        require_licenses=_RM_LICENSES,
        bypass_roles=[DirectoryRole.GlobalAdministrator],
    )
    def test_01_list_file_plan_descriptors(self):
        """Every file plan descriptor the client publishes returns a valid collection.

        The list is the five ``LabelsRoot`` navigations that exist - ``departments``,
        ``categories``, ``citations``, ``authorities``, ``filePlanReferences`` - rather than
        an invented ``subcategories``: Graph hangs a label's subcategory off the label, and
        the collection spelling of a reference is ``filePlanReferences``.
        """
        labels_root = self.client.security.labels
        for prop_name in ("departments", "categories", "citations", "authorities", "file_plan_references"):
            self.assertTrue(hasattr(labels_root, prop_name), f"the client no longer publishes '{prop_name}'")
            col = self.read(getattr(labels_root, prop_name))
            self.assertIsNotNone(col.resource_path, f"{prop_name} should return a valid collection")
