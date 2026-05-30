from typing import Optional

from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential
from office365.directory.serviceprincipals.service_principal import ServicePrincipal

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestServicePrincipal(GraphDelegatedTestCase):
    target_object: Optional[ServicePrincipal] = None
    password_creds: Optional[PasswordCredential] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_name: str = create_unique_name("App")
        cls.target_app: Application = cls.client.applications.add(app_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        if cls.target_app is not None:
            cls.target_app.delete_object(True).execute_query()

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test1_create_service_principal(self):
        """Create a service principal"""
        assert TestServicePrincipal.target_app is not None
        assert TestServicePrincipal.target_app.app_id is not None
        service_principal = self.client.service_principals.add(TestServicePrincipal.target_app.app_id).execute_query()
        self.assertIsNotNone(service_principal.resource_path)
        TestServicePrincipal.target_object = service_principal

    @requires_delegated(
        "Application.Read.All",
        "Application.ReadWrite.All",
        "Directory.Read.All",
        "Directory.ReadWrite.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test2_list_service_principals(self):
        """List service principals"""
        result = self.client.service_principals.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test3_get_service_principals_count(self):
        """Get service principals count"""
        result = self.client.service_principals.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Application.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test4_get_by_app_id(self):
        """Get service principal by app ID"""
        assert TestServicePrincipal.target_app is not None
        assert TestServicePrincipal.target_app.app_id is not None
        principal = (
            self.client.service_principals.get_by_app_id(TestServicePrincipal.target_app.app_id).get().execute_query()
        )
        self.assertIsNotNone(principal.resource_path)

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test5_add_password(self):
        """Add password to the service principal"""
        assert TestServicePrincipal.target_object is not None
        result = TestServicePrincipal.target_object.add_password("Password friendly name").execute_query()
        self.assertIsNotNone(result.value)
        TestServicePrincipal.password_creds = result.value

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test6_remove_password(self):
        """Remove password from the service principal"""
        assert TestServicePrincipal.password_creds is not None
        assert TestServicePrincipal.password_creds.keyId is not None
        assert TestServicePrincipal.target_object is not None
        TestServicePrincipal.target_object.remove_password(TestServicePrincipal.password_creds.keyId).execute_query()

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test7_delete_service_principal(self):
        """Delete the service principal"""
        assert TestServicePrincipal.target_object is not None
        TestServicePrincipal.target_object.delete_object().execute_query()

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test8_list_deleted(self):
        """List deleted service principals"""
        result = self.client.directory.deleted_service_principals.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreater(len(result), 0)
