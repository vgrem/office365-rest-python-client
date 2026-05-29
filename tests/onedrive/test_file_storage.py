from typing import Optional

from office365.onedrive.filestorage.container import FileStorageContainer
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFileStorage(GraphDelegatedTestCase):
    """File storage test case base class"""

    target_container: Optional[FileStorageContainer] = None

    @requires_delegated("FileStorageContainer.Selected", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test1_create_file_storage_container(self):
        """Create a file storage container"""
        result = self.client.storage.file_storage.containers.add("My Application Storage Container").execute_query()
        assert result.resource_path is not None
        TestFileStorage.target_container = result

    @requires_delegated("FileStorageContainer.Selected", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test2_create_container(self):
        """Create a file storage container with display name"""
        result = self.client.storage.file_storage.containers.add(
            display_name="My Application Storage Container"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated("FileStorageContainer.Selected", or_roles=["Global Administrator", "SharePoint Administrator"])
    def test3_list_containers(self):
        """List all file storage containers"""
        result = self.client.storage.file_storage.containers.get().execute_query()
        self.assertIsNotNone(result.resource_path)
