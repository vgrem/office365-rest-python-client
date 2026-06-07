"""Applications — listing, templates, creation, password management, and deletion.

Tests cover:
  - Listing applications
  - Listing application templates
  - Creating an application
  - Getting the applications count
  - Adding a password to the application
  - Removing a password from the application
  - Deleting the application
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.applications.application import Application
from office365.directory.password_credential import PasswordCredential

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestApplication(GraphDelegatedTestCase):
    """Application CRUD and password management."""

    target_app: ClassVar[Optional[Application]] = None
    target_password: ClassVar[Optional[PasswordCredential]] = None

    @requires_delegated(
        "Application.Read.All",
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_01_list_apps(self):
        """Listing applications returns a valid collection."""
        result = self.client.applications.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Application.Read.All",
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_02_list_templates(self):
        """Listing application templates returns a valid collection."""
        result = self.client.application_templates.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_03_create_app(self):
        """Creating an application returns a valid resource with an ID."""
        app_name = create_unique_name("App")
        new_app = self.client.applications.add(app_name).execute_query()
        self.assertIsNotNone(new_app.resource_path)
        self.assertIsNotNone(new_app.get_property("id"))
        self.assertEqual(new_app.get_property("displayName"), app_name)
        TestApplication.target_app = new_app

    @requires_delegated(
        "Application.Read.All",
        "Directory.Read.All",
        bypass_roles=[
            "Application Administrator",
            "Cloud Application Administrator",
            "Global Administrator",
            "Global Reader",
        ],
    )
    def test_04_get_apps_count(self):
        """Getting the applications count returns a numeric value."""
        result = self.client.applications.count().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_05_add_password(self):
        """Adding a password to the application returns a secret text."""
        app = TestApplication.target_app
        if not app:
            self.skipTest("No target application created from previous test")
        result = app.add_password("New password").execute_query()
        self.assertIsNotNone(result.value.secretText)
        TestApplication.target_password = result.value

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_06_remove_password(self):
        """Removing a password from the application succeeds."""
        app = TestApplication.target_app
        password = TestApplication.target_password
        if not app:
            self.skipTest("No target application")
        if not password:
            self.skipTest("No password to remove")
        key_id = password.keyId
        if not key_id:
            self.skipTest("Password has no keyId")
        app.remove_password(key_id).execute_query()

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_07_delete_app(self):
        """Deleting the application succeeds."""
        app = TestApplication.target_app
        if not app:
            self.skipTest("No target application to delete")
        app.delete_object(True).execute_query()
        TestApplication.target_app = None

    @classmethod
    def tearDownClass(cls):
        app = cls.target_app
        if app and app.resource_path:
            try:
                app.delete_object(True).execute_query()
            except Exception:
                pass
        cls.target_app = None
        cls.target_password = None
