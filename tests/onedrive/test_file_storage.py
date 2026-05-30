import uuid
from typing import Optional

from office365.onedrive.filestorage.container import FileStorageContainer
from tests import test_client_id
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFileStorage(GraphDelegatedTestCase):
    """File storage test case base class"""

    target_container: Optional[FileStorageContainer] = None
    container_type_id: str | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        types = cls.client.storage.file_storage.container_types.get().execute_query()
        if len(types) > 0:
            cls.container_type_id = types[0].id
        else:
            ct = cls.client.storage.file_storage.container_types.add(
                "Test Container Type", test_client_id, billing_classification="trial"
            ).execute_query()
            cls.container_type_id = ct.id

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test1_create_file_storage_container(self):
        """Create a file storage container"""
        assert self.container_type_id is not None
        result = self.client.storage.file_storage.containers.add(
            "My Application Storage Container", uuid.UUID(self.container_type_id)
        ).execute_query()
        assert result.resource_path is not None
        TestFileStorage.target_container = result

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test2_create_container(self):
        """Create a file storage container with display name"""
        assert self.container_type_id is not None
        result = self.client.storage.file_storage.containers.add(
            display_name="My Application Storage Container",
            container_type_id=uuid.UUID(self.container_type_id),
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Administrator"]
    )
    def test3_list_containers(self):
        """List all file storage containers"""
        result = self.client.storage.file_storage.containers.get().execute_query()
        self.assertIsNotNone(result.resource_path)
