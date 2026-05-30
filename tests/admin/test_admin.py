from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestAdmin(GraphDelegatedTestCase):
    """SharePoint specific test case base class"""

    @requires_delegated(
        "SharePointTenantSettings.Read.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test1_get_sharepoint_settings(self):
        result = self.client.admin.sharepoint.settings.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "SharePointTenantSettings.ReadWrite.All",
        bypass_roles=["SharePoint Administrator", "Global Administrator"],
    )
    def test2_update_sharepoint_settings(self):
        settings = self.client.admin.sharepoint.settings
        settings.sharing_blocked_domain_list = ["contoso.com", "fabrikam.com"]
        settings.update().execute_query()

    @requires_delegated(
        "ServiceMessage.Read.All",
        "ServiceHealth.Read.All",
        bypass_roles=["Service Support Administrator", "Global Administrator", "Global Reader"],
    )
    def test3_list_issues(self):
        result = self.client.admin.service_announcement.issues.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_delegated(
        "OrgSettings.Read.All",
        bypass_roles=["Reports Administrator", "Global Administrator", "Global Reader"],
    )
    def test4_list_microsoft365_apps(self):
        result = self.client.admin.microsoft365_apps.get().execute_query()
        self.assertIsNotNone(result.resource_path)

    # def test5_get_admin_people(self):
    #    result = self.client.admin.people.get().execute_query()
    #    self.assertIsNotNone(result.resource_path)
