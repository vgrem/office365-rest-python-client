from typing import Optional

from office365.directory.applications.application import Application
from office365.directory.extensions.extension_property import ExtensionProperty

from tests import create_unique_name
from tests.graph_case import GraphDelegatedTestCase


class TestExtensions(GraphDelegatedTestCase):
    target_app: Optional[Application] = None
    target_extension: Optional[ExtensionProperty] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_name = create_unique_name("App")
        cls.target_app = cls.client.applications.add(app_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        if cls.target_app is not None:
            cls.target_app.delete_object(True).execute_query()

    def test1_create_extension(self):
        """Create an extension property on the application"""
        assert TestExtensions.target_app is not None
        new_extension = TestExtensions.target_app.extension_properties.add(name="extensionName").execute_query()
        self.assertIsNotNone(new_extension.resource_path)
        TestExtensions.target_extension = new_extension

    def test2_list_extensions(self):
        """List available extension properties"""
        result = self.client.directory_objects.get_available_extension_properties(False).execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_delete_extension(self):
        """Delete the extension property"""
        assert TestExtensions.target_extension is not None
        TestExtensions.target_extension.delete_object().execute_query()
