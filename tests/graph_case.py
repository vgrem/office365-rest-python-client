from unittest import TestCase

from office365.graph_client import GraphClient

from tests import test_client_id, test_client_secret, test_password, test_tenant, test_username


class GraphTestCase(TestCase):
    """Microsoft Graph specific test case base class"""

    client: GraphClient = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        if test_username == "x" or test_password == "x":
            raise EnvironmentError("The environment variable 'office365_python_sdk_securevars' is not set.")

        cls.client = GraphClient(tenant=test_tenant).with_username_and_password(
            test_client_id, test_username, test_password
        )


class GraphSecretTestCase(GraphTestCase):
    """Microsoft Graph specific test case base class using client secret authentication"""

    @classmethod
    def setUpClass(cls):
        cls.client = GraphClient(tenant=test_tenant).with_client_secret(test_client_id, test_client_secret)
