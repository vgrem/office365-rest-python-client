from typing import Optional

from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential

from tests import create_unique_name
from tests.graph_case import GraphDelegatedTestCase


class TestApplication(GraphDelegatedTestCase):
    target_app: Optional[Application] = None
    target_password: Optional[PasswordCredential] = None

    def test1_list_apps(self):
        """List applications"""
        result = self.client.applications.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test2_list_templates(self):
        """List application templates"""
        result = self.client.application_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_create_app(self):
        """Create an application"""
        app_name = create_unique_name("App")
        new_app = self.client.applications.add(app_name).execute_query()
        self.assertIsNotNone(new_app.resource_path)
        TestApplication.target_app = new_app

    def test4_get_apps_count(self):
        """Get applications count"""
        result = self.client.applications.count().execute_query()
        self.assertIsNotNone(result.value)

    def test5_add_password(self):
        """Add password to the application"""
        assert TestApplication.target_app is not None
        result = TestApplication.target_app.add_password("New password").execute_query()
        self.assertIsNotNone(result.value.secretText)
        TestApplication.target_password = result.value

    def test6_remove_password(self):
        """Remove password from the application"""
        assert TestApplication.target_app is not None
        assert TestApplication.target_password is not None
        assert TestApplication.target_password.keyId is not None
        TestApplication.target_app.remove_password(TestApplication.target_password.keyId).execute_query()

    def test7_delete_app(self):
        """Delete the application"""
        assert TestApplication.target_app is not None
        result = TestApplication.target_app
        result.delete_object(True).execute_query()
