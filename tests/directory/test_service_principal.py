"""Service principals — CRUD, app ID lookup, password management, and deleted items.

Tests cover:
  - Creating a service principal
  - Listing service principals
  - Getting the service principals count
  - Getting a service principal by app ID
  - Adding a password to the service principal
  - Removing a password from the service principal
  - Deleting the service principal
  - Listing deleted service principals
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential
from office365.directory.serviceprincipals.service_principal import ServicePrincipal

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestServicePrincipal(GraphDelegatedTestCase):
    """Service principal CRUD, password management, and deleted items."""

    target_object: ClassVar[Optional[ServicePrincipal]] = None
    password_creds: ClassVar[Optional[PasswordCredential]] = None
    target_app: ClassVar[Optional[Application]] = None

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        app_name = create_unique_name("App")
        cls.target_app = cls.client.applications.add(app_name).execute_query()

    @classmethod
    def tearDownClass(cls):
        app = cls.target_app
        if app and app.resource_path:
            try:
                app.delete_object(True).execute_query()
            except Exception:
                pass
        cls.target_app = None
        cls.target_object = None
        cls.password_creds = None

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_01_create_service_principal(self):
        """Creating a service principal from an app returns a valid resource."""
        app = TestServicePrincipal.target_app
        if not app:
            self.skipTest("No target app created in setUpClass")
        app_id = app.app_id
        if not app_id:
            self.skipTest("Target app has no app_id")
        service_principal = self.client.service_principals.add(app_id).execute_query()
        self.assertIsNotNone(service_principal.resource_path)
        self.assertIsNotNone(service_principal.get_property("id"))
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
    def test_02_list_service_principals(self):
        """Listing service principals returns a valid collection."""
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
    def test_03_get_service_principals_count(self):
        """Getting the service principals count returns a numeric value."""
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
    def test_04_get_by_app_id(self):
        """Getting a service principal by app ID returns a valid resource."""
        app = TestServicePrincipal.target_app
        if not app:
            self.skipTest("No target app created in setUpClass")
        app_id = app.app_id
        if not app_id:
            self.skipTest("Target app has no app_id")
        principal = self.client.service_principals.get_by_app_id(app_id).get().execute_query()
        self.assertIsNotNone(principal.resource_path)

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_05_add_password(self):
        """Adding a password to the service principal returns credentials."""
        sp = TestServicePrincipal.target_object
        if not sp:
            self.skipTest("No target service principal created")
        result = sp.add_password("Password friendly name").execute_query()
        self.assertIsNotNone(result.value)
        TestServicePrincipal.password_creds = result.value

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_06_remove_password(self):
        """Removing a password from the service principal succeeds."""
        sp = TestServicePrincipal.target_object
        password = TestServicePrincipal.password_creds
        if not sp:
            self.skipTest("No target service principal")
        if not password:
            self.skipTest("No password credentials to remove")
        key_id = password.keyId
        if not key_id:
            self.skipTest("Password has no keyId")
        sp.remove_password(key_id).execute_query()

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_07_delete_service_principal(self):
        """Deleting the service principal succeeds."""
        sp = TestServicePrincipal.target_object
        if not sp:
            self.skipTest("No target service principal to delete")
        sp.delete_object().execute_query()

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_08_list_deleted(self):
        """Listing deleted service principals returns at least one entry."""
        result = self.client.directory.deleted_service_principals.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreater(len(result), 0)
