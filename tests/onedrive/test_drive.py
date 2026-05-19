from tests.decorators import requires_delegated_permission_or_role
from tests.graph_case import GraphDelegatedTestCase


class TestDrive(GraphDelegatedTestCase):
    """OneDrive specific test case base class"""

    @requires_delegated_permission_or_role(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test1_list_drives(self):
        """List all drives"""
        drives = self.client.drives.top(2).get().execute_query()
        self.assertLessEqual(len(drives), 2)
        for drive in drives:
            self.assertIsNotNone(drive.web_url)

    @requires_delegated_permission_or_role(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test2_list_drives_alt(self):
        """List drives using direct request"""
        resp = self.client.execute_request_direct("drives?$top=2")
        drives = resp.json()["value"]
        self.assertLessEqual(len(drives), 2)
        for drive in drives:
            self.assertIsNotNone(drive["webUrl"])

    @requires_delegated_permission_or_role(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test4_get_drive_root(self):
        """Get the root of the current drive"""
        result = self.client.me.drive.root.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated_permission_or_role(
        "Files.Read",
        "Files.Read.All",
        "Files.ReadWrite",
        "Files.ReadWrite.All",
        "Sites.Read.All",
        "Sites.ReadWrite.All",
        roles=["Global Administrator"],
    )
    def test5_get_recent(self):
        """Get recently used items"""
        items = self.client.me.drive.recent().execute_query()
        self.assertIsNotNone(items.resource_path)

    def test4_search_drive(self):
        """Search for files in the drive"""
        items = self.client.me.drive.search("Guide.docx").execute_query()
        self.assertIsNotNone(items.resource_path)

    def test5_shared_with_me(self):
        """Get items shared with the current user"""
        col = self.client.me.drive.shared_with_me().execute_query()
        self.assertIsNotNone(col.resource_path)

    # def test6_list_bundles(self):
    #    result = self.client.me.drive.bundles.get().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    def test7_list_changes(self):
        """List drive changes"""
        result = self.client.me.drive.root.delta.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test8_get_delta_link(self):
    #    result = self.client.me.drive.root.delta().token("latest").get().execute_query()
    #    self.assertIsNotNone(result.resource_path)
