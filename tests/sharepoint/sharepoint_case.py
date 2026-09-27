from __future__ import annotations

from unittest import TestCase

from office365.sharepoint.client_context import ClientContext

from tests import (
    test_cert_path,
    test_cert_thumbprint,
    test_client_id,
    test_client_secret,
    test_team_site_url,
    test_tenant,
)


class SPTestCase(TestCase):
    """SharePoint specific test case base class"""

    @classmethod
    def setUpClass(cls):
        if test_client_secret == "x":
            raise EnvironmentError(
                "Credentials are not configured. Add OFFICE365_* values to .env at the project "
                "root (see CONTRIBUTING.md), or run with --offline."
            )

        # cls.client = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)
        cls.client: ClientContext = ClientContext(test_team_site_url).with_client_certificate(
            test_tenant,
            client_id=test_client_id,
            thumbprint=test_cert_thumbprint,
            cert_path=test_cert_path,
        )
