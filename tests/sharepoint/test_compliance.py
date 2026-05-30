from __future__ import annotations

from office365.sharepoint.listitems.listitem import ListItem
from office365.sharepoint.lists.list import List

from tests.sharepoint.sharepoint_case import SPTestCase


class TestCompliance(SPTestCase):
    list_item: ListItem | None = None
    tag_name: str | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_list: List = cls.client.web.lists.get_by_title("Documents")

    def test1_get_site_available_tags(self):
        result = self.client.site.get_available_tags().execute_query()
        self.assertIsNotNone(result.value)
        if len(result.value) > 0:
            TestCompliance.tag_name = result.value[0].TagName

    def test_2_set_list_compliance_tag(self):
        if TestCompliance.tag_name is None:
            self.skipTest("No compliance tags available on this tenant")
        result = self.target_list.set_compliance_tag(TestCompliance.tag_name, True, True, True).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test_3_get_list_compliance_tag(self):
        result = self.target_list.get_compliance_tag().execute_query()
        self.assertIsNotNone(result.value)

    # def test_4_reset_list_compliance_tag(self):
    #    result = self.target_list.set_compliance_tag(
    #        "", False, False, False
    #    ).execute_query()
    #    self.assertIsNotNone(result.value)

    # def test_5_enable_place_record_management(self):
    #    result = self.client.site.features.add(
    #        KnownFeaturesList.PlaceRecordsManagement, False, FeatureDefinitionScope.Site
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test_6_lock_record_item(self):
    #    result = self.list_item.lock_record_item().execute_query()
    #    self.assertIsNotNone(result.resource_path)
