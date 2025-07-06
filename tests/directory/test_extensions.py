from office365.directory.applications.application import Application
from office365.directory.extensions.extension_property import ExtensionProperty
from tests import create_unique_name
from tests.graph_case import GraphTestCase


class TestExtensions(GraphTestCase):
    target_app: Application = None
    target_extension: ExtensionProperty = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_name = create_unique_name("App")
        cls.target_app = cls.client.applications.add(app_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_app.delete_object(True).execute_query()

    def test1_create_extension(self):
        new_extension = self.__class__.target_app.extension_properties.add(
            name="extensionName"
        ).execute_query()
        self.assertIsNotNone(new_extension.resource_path)
        self.__class__.target_extension = new_extension

    def test2_list_extensions(self):
        result = self.client.directory_objects.get_available_extension_properties(
            False
        ).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_delete_extension(self):
        self.target_extension.delete_object().execute_query()
