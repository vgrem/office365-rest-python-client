from unittest import TestCase

from office365.sharepoint.client_context import ClientContext
from office365.sharepoint.tenant.administration.tenant import Tenant
from tests import test_admin_credentials, test_admin_site_url


class TestHomeSites(TestCase):
    @classmethod
    def setUpClass(cls):
        client = ClientContext(test_admin_site_url).with_credentials(
            test_admin_credentials
        )
        cls.tenant = Tenant(client)

    def test1_get_home_sites(self):
        result = self.tenant.get_home_sites().execute_query()
        self.assertIsNotNone(result.value)
