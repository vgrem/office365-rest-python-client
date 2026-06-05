"""Mail folders — creating, listing, updating, and permanent deletion.

Tests cover:
  - Creating a mail folder as a child of inbox
  - Listing mail folders with minimum count verification
  - Updating a mail folder
  - Permanently deleting a mail folder
  - Folder property assertions (displayName, parentFolderId)
"""

from __future__ import annotations

from typing import ClassVar, Optional

from office365.outlook.mail.folders.folder import MailFolder

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestMailFolders(GraphDelegatedTestCase):
    """Mail folder CRUD and lifecycle."""

    target_folder: ClassVar[Optional[MailFolder]] = None

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_01_create_mail_folder(self):
        """Creating a mail folder with a display name should succeed."""
        result = self.client.me.mail_folders.add("SDK_Test_MailFolder", True).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), "SDK_Test_MailFolder")
        TestMailFolders.target_folder = result

    @requires_delegated(
        "Mail.ReadBasic", "Mail.Read", "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_02_list_mail_folders(self):
        """Listing mail folders returns at least one result (inbox)."""
        result = self.client.me.mail_folders.get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertGreaterEqual(len(result), 1)

    @requires_delegated(
        "Mail.ReadBasic", "Mail.Read", "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_03_folder_has_expected_properties(self):
        """A mail folder exposes displayName, parentFolderId, and childFolderCount."""
        folder = TestMailFolders.target_folder
        if not folder:
            self.skipTest("No folder created from previous test")

        self.assertIsNotNone(folder.get_property("displayName"))
        self.assertIsNotNone(folder.get_property("parentFolderId"))
        self.assertIsNotNone(folder.get_property("childFolderCount"))

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_04_update_mail_folder(self):
        """Updating a mail folder should not error."""
        folder = TestMailFolders.target_folder
        if not folder:
            self.skipTest("No folder created from previous test")

        folder.update().execute_query()
        self.assertIsNotNone(folder.resource_path)

    @requires_delegated(
        "Mail.ReadWrite",
        bypass_roles=["Exchange Administrator", "Global Administrator"],
    )
    def test_05_permanent_delete_mail_folder(self):
        """Permanently deleting a mail folder removes it."""
        folder = TestMailFolders.target_folder
        if not folder:
            self.skipTest("No folder created from previous test")

        folder.permanent_delete().execute_query()
        TestMailFolders.target_folder = None

    @classmethod
    def tearDownClass(cls):
        folder = cls.target_folder
        if folder and folder.resource_path:
            try:
                folder.permanent_delete().execute_query()
            except Exception:
                pass
