"""OneDrive drives — listing, root, recent, search, shared, changes.

Tests cover:
  - Listing drives with pagination
  - Getting the current user's drive root
  - Getting recently used items
  - Searching for files in the drive
  - Listing items shared with the user
  - Listing drive changes via delta
"""

from __future__ import annotations

from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestDrive(GraphDelegatedTestCase):
    """OneDrive drive operations — listing, root, recent, search, shared, changes."""

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_01_list_drives(self):
        """Listing all drives with $top=2 returns a valid collection."""
        drives = self.client.drives.top(2).get().execute_query()
        self.assertLessEqual(len(drives), 2)
        for drive in drives:
            self.assertIsNotNone(drive.get_property("webUrl"))

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_02_get_drive_root(self):
        """Getting the drive root returns a valid item."""
        result = self.client.me.drive.root.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_03_get_recent_items(self):
        """Getting recently used items returns a valid collection."""
        items = self.client.me.drive.recent().execute_query()
        self.assertIsNotNone(items.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_04_search_drive(self):
        """Searching for files in the drive by keyword returns results."""
        items = self.client.me.drive.search("Guide.docx").execute_query()
        self.assertIsNotNone(items.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_05_shared_with_me(self):
        """Listing items shared with the current user returns a valid collection."""
        col = self.client.me.drive.shared_with_me().execute_query()
        self.assertIsNotNone(col.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_06_list_changes(self):
        """Listing drive changes via delta returns a valid collection."""
        result = self.client.me.drive.root.delta.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        bypass_roles=["Global Administrator", "SharePoint Administrator"],
    )
    def test_07_drive_has_expected_properties(self):
        """A drive exposes id, driveType, and webUrl."""
        drives = self.client.drives.top(1).get().execute_query()
        if len(drives) > 0:
            drive = drives[0]
            self.assertIsNotNone(drive.id)
            self.assertIsNotNone(drive.drive_type)
            self.assertIsNotNone(drive.web_url)
