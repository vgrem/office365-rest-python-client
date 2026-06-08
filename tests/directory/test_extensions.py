"""Extension properties — creation, listing, and deletion on an application.

Tests cover:
  - Creating an extension property on an application
  - Listing available extension properties
  - Deleting the extension property
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.directory.applications.application import Application
from office365.directory.extensions.extension_property import ExtensionProperty

from tests import create_unique_name
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestExtensions(GraphDelegatedTestCase):
    """Extension property CRUD on an application."""

    target_app: ClassVar[Optional[Application]] = None
    target_extension: ClassVar[Optional[ExtensionProperty]] = None

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
        cls.target_extension = None

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_01_create_extension(self):
        """Creating an extension property on the application returns a valid resource."""
        app = TestExtensions.target_app
        if not app:
            self.skipTest("No target app created in setUpClass")
        new_extension = app.extension_properties.add(name="extensionName").execute_query()
        self.assertIsNotNone(new_extension.resource_path)
        self.assertIsNotNone(new_extension.id)
        TestExtensions.target_extension = new_extension

    @requires_delegated(
        "Directory.Read.All",
        bypass_roles=["Global Reader", "Global Administrator"],
    )
    def test_02_list_extensions(self):
        """Listing available extension properties returns a valid collection."""
        result = self.client.directory_objects.get_available_extension_properties(False).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Application.ReadWrite.All",
        "Directory.ReadWrite.All",
        bypass_roles=["Application Administrator", "Cloud Application Administrator", "Global Administrator"],
    )
    def test_03_delete_extension(self):
        """Deleting the extension property succeeds."""
        extension = TestExtensions.target_extension
        if not extension:
            self.skipTest("No extension created from previous test")
        extension.delete_object().execute_query()
