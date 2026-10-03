from __future__ import annotations

from unittest import TestCase

from office365.sharepoint.client_context import ClientContext

from tests.settings import settings


class SPTestCase(TestCase):
    """SharePoint specific test case base class"""

    @classmethod
    def setUpClass(cls):
        settings.require("app-only-cert")

        cls.client: ClientContext = ClientContext(settings.team_site_url).with_client_certificate(
            settings.tenant,
            client_id=settings.client_id,
            thumbprint=settings.cert_thumbprint,
            cert_path=settings.cert_path,
        )
