from office365.sharepoint.features.definitions.scope import FeatureDefinitionScope
from office365.sharepoint.features.known_list import KnownFeaturesList
from office365.sharepoint.lists.list import List
from tests.sharepoint.sharepoint_case import SPTestCase


class TestSharePointDocumentId(SPTestCase):
    target_lib: List = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_lib = cls.client.web.default_document_library()

    def test1_get_service(self):
        result = self.client.document_id.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test2_ensure_doc_id_feature(self):
    #    result = self.client.site.features.add(
    #        KnownFeaturesList.DocId, False, FeatureDefinitionScope.Farm
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)
