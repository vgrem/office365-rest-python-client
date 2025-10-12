from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential
from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from tests import create_unique_name
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestServicePrincipal(GraphTestCase):
    target_object: ServicePrincipal = None
    target_app: Application = None
    password_creds: PasswordCredential = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_name = create_unique_name("App")
        cls.target_app = cls.client.applications.add(app_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        cls.target_app.delete_object(True).execute_query()

    def test1_create_service_principal(self):
        service_principal = self.client.service_principals.add(self.target_app.app_id).execute_query()
        self.assertIsNotNone(service_principal.resource_path)
        self.__class__.target_object = service_principal

    @requires_delegated_permission(
        "Application.Read.All",
        "Application.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
    )
    def test2_list_service_principals(self):
        result = self.client.service_principals.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    def test3_get_service_principals_count(self):
        result = self.client.service_principals.count().execute_query()
        self.assertIsNotNone(result.value)

    def test4_get_by_app_id(self):
        principal = self.client.service_principals.get_by_app_id(self.target_app.app_id).get().execute_query()
        self.assertIsNotNone(principal.resource_path)

    def test5_add_password(self):
        result = self.__class__.target_object.add_password("Password friendly name").execute_query()
        self.assertIsNotNone(result.value)
        self.__class__.password_creds = result.value

    def test6_remove_password(self):
        key_id = self.__class__.password_creds.keyId
        self.__class__.target_object.remove_password(key_id).execute_query()

    def test7_delete_service_principal(self):
        self.__class__.target_object.delete_object().execute_query()

    def test8_list_deleted(self):
        result = self.__class__.client.directory.deleted_service_principals.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreater(len(result), 0)
