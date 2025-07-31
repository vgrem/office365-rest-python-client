from office365.directory.serviceprincipals.service_principal import ServicePrincipal
from tests import test_client_id
from tests.decorators import requires_delegated_permission
from tests.graph_case import GraphTestCase


class TestSynchronization(GraphTestCase):

    target_sp: ServicePrincipal = None

    # "salesforce"

    @classmethod
    def setUpClass(cls):
        super(TestSynchronization, cls).setUpClass()
        cls.target_sp = (
            cls.client.service_principals.get_by_app_id(test_client_id)
            .get()
            .execute_query()
        )

    @classmethod
    def tearDownClass(cls):
        pass

    @requires_delegated_permission(
        "Synchronization.Read.All", "Synchronization.ReadWrite.All"
    )
    def test1_list_synchronization_jobs(self):
        result = self.target_sp.synchronization.jobs.get().execute_query()
        self.assertIsNotNone(result.resource_path)
