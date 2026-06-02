from __future__ import annotations

from typing import Optional

from office365.graph_client import GraphClient
from office365.onedrive.filestorage.containers.container import FileStorageContainer
from tests import test_client_id, test_client_secret, test_tenant
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
            # Use app-only auth to discover and prepare the container type
            admin = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
            types = admin.storage.file_storage.container_types.get().execute_query()
            if types:
                cls.container_type_id = types[0].id
                # Grant FileStorageContainer.Selected so delegated tests can create containers
                registrations = admin.storage.file_storage.container_type_registrations.get().execute_query()
                reg = next((r for r in registrations if r.owning_app_id == test_client_id), None)
                if reg:
                    reg.grant_permissions(test_client_id).execute_query()
        except Exception:
            cls.container_type_id = None

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
