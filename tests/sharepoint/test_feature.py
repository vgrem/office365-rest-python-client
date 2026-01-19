from office365.sharepoint.features.feature import Feature

from tests.sharepoint.sharepoint_case import SPTestCase


class TestFeature(SPTestCase):
    result_feature: Feature = None

    def test1_list_site_features(self):
        result = self.client.site.features.get().execute_query()
        self.assertGreater(len(result), 0)
        self.__class__.result_feature = result[0]

    def test2_get_site_feature(self):
        result = self.result_feature.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_list_web_features(self):
        result = self.client.site.root_web.features.get().execute_query()
        self.assertGreater(len(result), 0)
