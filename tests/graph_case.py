from unittest import TestCase

from office365.graph_client import GraphClient

from tests.settings import settings


class GraphDelegatedTestCase(TestCase):
    """Microsoft Graph specific test case base class"""

    client: GraphClient = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        settings.require("delegated-ropc")

        cls.client = GraphClient(tenant=settings.tenant).with_username_and_password(
            settings.client_id, settings.username, settings.password
        )


class GraphApplicationTestCase(GraphDelegatedTestCase):
    """Microsoft Graph specific test case base class using client secret authentication"""

    @classmethod
    def setUpClass(cls):
        settings.require("app-only")

        cls.client = GraphClient(tenant=settings.tenant).with_client_secret(settings.client_id, settings.client_secret)
