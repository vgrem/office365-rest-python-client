from unittest import TestCase

from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_site_url, test_client_credentials


class TestReports(TestCase):
    tenant: Tenant = None

    @classmethod
    def setUpClass(cls):
        tenant = Tenant.from_url(test_admin_site_url).with_credentials(
            test_client_credentials
        )
        cls.tenant = tenant

    # def test1_get_top_files_sharing_insights(self):
    #    result = self.tenant.get_top_files_sharing_insights().execute_query()
    #    self.assertIsNotNone(result.resource_path)

    # def test2_render_recent_admin_actions(self):
    #  result = self.tenant.render_recent_admin_actions().execute_query()
    #  self.assertIsNotNone(result.value)
