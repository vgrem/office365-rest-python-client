from office365.onedrive.filestorage.container import FileStorageContainer
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestFileStorage(GraphTestCase):
    """File storage test case base class"""

    target_container = None  # type: FileStorageContainer

    @requires_delegated_permission("FileStorageContainer.Selected")
    def test1_create_file_storage_container(self):
        result = self.client.storage.file_storage.containers.add(
            "My Application Storage Container"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.__class__.target_container = result

    @requires_delegated_permission("FileStorageContainer.Selected")
    def test2_create_container(self):
        result = self.client.storage.file_storage.containers.add(
            display_name="My Application Storage Container"
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission("FileStorageContainer.Selected")
    def test3_list_containers(self):
        result = self.client.storage.file_storage.containers.get().execute_query()
        self.assertIsNotNone(result.resource_path)
