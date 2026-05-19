from tests.graph_case import GraphDelegatedTestCase


class TestSecurityReports(GraphDelegatedTestCase):
    # @requires_delegated_permission("AttackSimulation.Read.All")
    def test1_get_attack_simulation_repeat_offenders(self):
        result = self.client.reports.security.get_attack_simulation_repeat_offenders().execute_query()
        self.assertIsNotNone(result.value)

    def test2_get_attack_simulation_simulation_user_coverage(self):
        result = self.client.reports.security.get_attack_simulation_simulation_user_coverage().execute_query()
        self.assertIsNotNone(result.value)
