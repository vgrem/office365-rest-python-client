from unittest import TestCase

from office365.sharepoint.client_context import ClientContext

from tests import test_client_id, test_client_secret, test_team_site_url


class SPTestCase(TestCase):
    """SharePoint specific test case base class"""

    client: ClientContext = None  # type: ignore[assignment]

    @classmethod
    def setUpClass(cls):
        if test_client_secret == "x":
            raise EnvironmentError("The environment variable 'office365_python_sdk_securevars' is not set.")

        cls.client = ClientContext(test_team_site_url).with_client_credentials(test_client_id, test_client_secret)
