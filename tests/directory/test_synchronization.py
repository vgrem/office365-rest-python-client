from typing import Optional

from office365.directory.serviceprincipals.service_principal import ServicePrincipal

from tests import test_client_id
from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSynchronization(GraphDelegatedTestCase):
    target_sp: Optional[ServicePrincipal] = None

    # "salesforce"

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.target_sp = cls.client.service_principals.get_by_app_id(test_client_id).get().execute_query()

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated(
        "Synchronization.Read.All",
        "Synchronization.ReadWrite.All",
        or_roles=["Global Administrator"],
    )
    def test1_list_synchronization_jobs(self):
        """List synchronization jobs"""
        assert TestSynchronization.target_sp is not None
        result = TestSynchronization.target_sp.synchronization.jobs.get().execute_query()
        self.assertIsNotNone(result.resource_path)
