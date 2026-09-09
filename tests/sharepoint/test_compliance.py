"""Tests for SharePoint compliance operations (tags and records management)."""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.runtime.client_request_exception import ClientRequestException
from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List

from tests.sharepoint.sharepoint_case import SPTestCase


class TestCompliance(SPTestCase):
    """Tests for SharePoint compliance tag operations."""

    list_item: ClassVar[Optional[ListItem]] = None
    tag_name: ClassVar[Optional[str]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_list: List = cls.client.web.lists.get_by_title("Documents")

    def test_01_get_site_available_tags(self):
        """Get available compliance tags for the site."""
        result = self.client.site.get_available_tags().execute_query()
        self.assertIsNotNone(result.value)
        if len(result.value) > 0:
            TestCompliance.tag_name = result.value[0].TagName

    def test_02_enable_place_records_management(self):
        """Enable the Place Records Management feature at the site scope."""
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        result = self.client.site.features.add(
            KnownFeaturesList.PlaceRecordsManagement, False, FeatureDefinitionScope.Site, True
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_03_set_list_compliance_tag(self):
        """Apply a compliance tag to the target list."""
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        result = self.target_list.set_compliance_tag(TestCompliance.tag_name, True, True, True).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_04_get_list_compliance_tag(self):
        """Read back the compliance tag from the target list."""
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        result = self.target_list.get_compliance_tag().execute_query()
        self.assertIsNotNone(result.value)
        self.assertEqual(result.value.TagName, TestCompliance.tag_name)

    def test_05_reset_list_compliance_tag(self):
        """Reset (remove) the compliance tag from the target list."""
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        result = self.target_list.set_compliance_tag("", False, False, False).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_06_get_list_compliance_tag_after_reset(self):
        """Verify the compliance tag has been removed from the target list."""
        result = self.target_list.get_compliance_tag().execute_query()
        self.assertIsNotNone(result.value)
        self.assertFalse(result.value.TagName)

    def test_07_set_item_compliance_tag_with_hold(self):
        """Apply a compliance tag with hold to a list item."""
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        TestCompliance.list_item = self._get_target_item()
        if TestCompliance.list_item is None:
            self.skipTest("No items available in the target list")
        try:
            result = TestCompliance.list_item.set_compliance_tag_with_hold(TestCompliance.tag_name).execute_query()
            self.assertIsNotNone(result.resource_path)
        except ClientRequestException as e:
            self.skipTest(f"Tag with hold is not supported for the current site: {e}")

    def test_08_lock_record_item(self):
        """Lock a record item to prevent modifications."""
        if TestCompliance.list_item is None:
            self.skipTest("No list item is available to lock")
        try:
            result = TestCompliance.list_item.lock_record_item().execute_query()
            self.assertIsNotNone(result.value)
        except ClientRequestException as e:
            self.skipTest(f"Record locking is not available for the current item: {e}")

    def _get_target_item(self) -> Optional[ListItem]:
        """Returns the first item of the target list, or None when the list is empty."""
        result = self.target_list.items.top(1).get().execute_query()
        if len(result) > 0:
            return result[0]
        return None
