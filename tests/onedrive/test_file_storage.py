from __future__ import annotations

from typing import Optional

from office365.onedrive.filestorage.containers.container import FileStorageContainer
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFileStorage(GraphDelegatedTestCase):
    """File storage test case base class"""

    target_container: Optional[FileStorageContainer] = None
    container_type_id: str | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        try:
            types = cls.client.storage.file_storage.container_types.get().execute_query()
            if types:
                cls.container_type_id = types[0].id
        except Exception:
            cls.container_type_id = "63003f1c-3b31-4779-847a-5b2b3a9a47a0"

    @requires_delegated(
        "FileStorageContainerType.Manage.All", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test1_create_file_storage_container(self):
        """Create a file storage container"""
        if self.container_type_id is None:
            self.skipTest("No container type available")
        result = self.client.storage.file_storage.containers.add(
            "My Application Storage Container", self.container_type_id
        ).execute_query()
        assert result.resource_path is not None
        TestFileStorage.target_container = result

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test3_list_containers(self):
        """List all file storage containers"""
        if self.container_type_id is None:
            self.skipTest("No container type available")
        result = self.client.storage.file_storage.containers.get_by_container_type_id(
            self.container_type_id
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
