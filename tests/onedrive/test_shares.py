import os

from tests import test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestShares(GraphDelegatedTestCase):
    """Shares API specific test case"""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        path = f"{os.path.dirname(__file__)}/../data/Financial Sample.xlsx"
        cls.file_item = cls.client.sites.get_by_url(test_team_site_url).drive.root.upload_file(path).execute_query()
        assert cls.file_item.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        cls.file_item.delete_object().execute_query_retry()

    @requires_delegated(
        "Files.Read", "Files.Read.All", "Files.ReadWrite", "Files.ReadWrite.All", or_roles=["Global Administrator"]
    )
    def test1_get_file_by_abs_url(self):
        """Get a file by its absolute URL"""
        file_abs_url = f"{test_team_site_url}/Shared Documents/Financial Sample.xlsx"
        result = self.client.shares.by_url(file_abs_url).drive_item.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertTrue(result.is_file)
