from __future__ import annotations

import uuid
from typing import Optional

from office365.onedrive.filestorage.container import FileStorageContainer
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
            cls.container_type_id = types[0].id if len(types) > 0 else None
        except Exception:
            cls.container_type_id = None

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test1_create_file_storage_container(self):
        """Create a file storage container"""
        if self.container_type_id is None:
            self.skipTest("No container type — grant FileStorageContainerType.Manage.All")
        result = self.client.storage.file_storage.containers.add(
            "My Application Storage Container", uuid.UUID(self.container_type_id)
        ).execute_query()
        assert result.resource_path is not None
        TestFileStorage.target_container = result

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test2_create_container(self):
        """Create a file storage container with display name"""
        if self.container_type_id is None:
            self.skipTest("No container type — grant FileStorageContainerType.Manage.All")
        result = self.client.storage.file_storage.containers.add(
            display_name="My Application Storage Container",
            container_type_id=uuid.UUID(self.container_type_id),
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test3_list_containers(self):
        """List all file storage containers"""
        if self.container_type_id is None:
            self.skipTest("No container type — grant FileStorageContainerType.Manage.All")
        result = self.client.storage.file_storage.containers.get_by_container_type_id(
            self.container_type_id
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
