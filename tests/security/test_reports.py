from tests.decorators import requires_delegated
from tests.graph_case import GraphDelegatedTestCase


class TestSecurityReports(GraphDelegatedTestCase):
    @requires_delegated("AttackSimulation.Read.All", bypass_roles=["Global Administrator"])
    def test1_get_attack_simulation_repeat_offenders(self):
        """Get attack simulation repeat offenders report."""
        result = self.client.reports.security.get_attack_simulation_repeat_offenders().execute_query()
        self.assertIsNotNone(result.value)

    @requires_delegated("AttackSimulation.Read.All", bypass_roles=["Global Administrator"])
    def test2_get_attack_simulation_simulation_user_coverage(self):
        """Get attack simulation user coverage report."""
        result = self.client.reports.security.get_attack_simulation_simulation_user_coverage().execute_query()
        self.assertIsNotNone(result.value)
