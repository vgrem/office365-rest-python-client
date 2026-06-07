from __future__ import annotations

from unittest import TestCase

from office365.sharepoint.client_context import ClientContext

from tests import test_client_id, test_client_secret, test_team_site_url, test_tenant, test_cert_thumbprint, \
    test_cert_path


class SPTestCase(TestCase):
    """SharePoint specific test case base class"""

    @classmethod
    def setUpClass(cls):
        if test_client_secret == "x":
            raise EnvironmentError("The environment variable 'office365_python_sdk_securevars' is not set.")

        # cls.client = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)
        cls.client: ClientContext = ClientContext(test_team_site_url).with_client_certificate(
            test_tenant,
            client_id=test_client_id,
            thumbprint=test_cert_thumbprint,
            cert_path=test_cert_path,
        )
