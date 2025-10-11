from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential
from tests import create_unique_name
from tests.graph_case import GraphTestCase


class TestApplication(GraphTestCase):
    target_app: Application = None
    target_password: PasswordCredential = None

    def test1_list_apps(self):
        result = self.client.applications.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test2_list_templates(self):
        result = self.client.application_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_create_app(self):
        app_name = create_unique_name("App")
        new_app = self.client.applications.add(app_name).execute_query()
        self.assertIsNotNone(new_app.resource_path)
        self.__class__.target_app = new_app

    def test4_get_apps_count(self):
        result = self.client.applications.count().execute_query()
        self.assertIsNotNone(result.value)

    def test5_add_password(self):
        result = self.__class__.target_app.add_password("New password").execute_query()
        self.assertIsNotNone(result.value.secretText)
        self.__class__.target_password = result.value

    def test6_remove_password(self):
        self.__class__.target_app.remove_password(self.__class__.target_password.keyId).execute_query()

    def test7_delete_app(self):
        result = self.__class__.target_app
        result.delete_object(True).execute_query()
