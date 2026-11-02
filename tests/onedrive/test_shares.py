import shutil
import tempfile
from pathlib import Path
from typing import ClassVar

from tests import DATA_DIR, create_unique_file_name, test_team_site_url
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestShares(GraphDelegatedTestCase):
    """Shares API specific test case"""

    file_name: ClassVar[str] = ""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # A uniquely named throwaway: the fixed fixture name is whatever an earlier run left
        # behind, and a shared-locked copy refuses the overwrite outright with
        # 'notAllowed', 'This operation has been disabled by policy'.
        cls.file_name = create_unique_file_name("SDK Shares ", "xlsx")
        source = DATA_DIR / "Financial Sample.xlsx"
        target = Path(tempfile.mkdtemp(prefix="o365-shares-")) / cls.file_name
        shutil.copyfile(source, target)
        cls.file_item = (
            cls.client.sites.get_by_url(test_team_site_url).drive.root.upload_file(str(target)).execute_query()
        )
        assert cls.file_item.resource_path is not None

    @classmethod
    def tearDownClass(cls):
        cls.file_item.delete_object(bypass_shared_lock=True).execute_query_retry()

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test1_get_file_by_abs_url(self):
        """Get a file by its absolute URL"""
        file_abs_url = f"{test_team_site_url}/Shared Documents/{self.file_name}"
        result = self.client.shares.by_url(file_abs_url).drive_item.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertTrue(result.is_file)
