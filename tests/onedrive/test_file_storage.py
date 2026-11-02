from __future__ import annotations

from typing import Optional

from office365.onedrive.filestorage.containers.container import FileStorageContainer
from office365.runtime.client_request_exception import ClientRequestException
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestFileStorage(GraphDelegatedTestCase):
    """File storage test case base class"""

    target_container: Optional[FileStorageContainer] = None
    container_type_id: str | None = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # The container type is the tenant's own; a made-up id filters to nothing, so the
        # suite reads the first one it is offered and skips when the tenant offers none.
        types = cls.client.storage.file_storage.container_types.get().execute_query()
        cls.container_type_id = types[0].id if len(types) else None

    @requires_delegated(
        "FileStorageContainerType.Manage.All", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test1_create_file_storage_container(self):
        """Create a file storage container"""
        if self.container_type_id is None:
            self.skipTest("No container type available")
        try:
            result = self.client.storage.file_storage.containers.add(
                "My Application Storage Container", self.container_type_id
            ).execute_query()
        except ClientRequestException as error:
            # Measured: a delegated (public-client) token is refused outright - container
            # creation is an app-only operation - so the skip names the rule, not a grant.
            if "Container creation by a public client is not allowed" not in str(error):
                raise
            self.skipTest(f"container creation needs an app-only token: {error}")
        assert result.resource_path is not None
        TestFileStorage.target_container = result

    @requires_delegated(
        "FileStorageContainer.Selected", bypass_roles=["Global Administrator", "SharePoint Embedded Administrator"]
    )
    def test3_list_containers(self):
        """List all file storage containers"""
        if self.container_type_id is None:
            self.skipTest("No container type available")
        result = (
            self.client.storage.file_storage.containers.by_container_type_id(self.container_type_id)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
