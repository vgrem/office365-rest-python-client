from tests.decorators import requires_application
from tests.graph_case import GraphApplicationTestCase


class TestSecurity(GraphApplicationTestCase):
    # def test1_create_alert(self):
    #    result = self.client.security.alerts.add(
    #        "Simulated Phishing Alert",
    #        "This is a test alert for simulation purposes.",
    #        "high",
    #        "ThreatManagement",
    #        "newAlert",
    #        "Custom",
    #        {"provider": "CustomProvider", "providerVersion": "1.0"},
    #    ).execute_query()
    #    self.assertIsNotNone(result.resource_path)

    @requires_application("AttackSimulation.ReadWrite.All")
    def test2_create_simulations(self):
        """Create attack simulation."""
        simulation = {
            "displayName": "Test Phishing Campaign",
            "payloadDeliveryPlatform": "email",
            "durationInDays": 3,
            "attackTechnique": "credentialHarvesting",
            "status": "scheduled",
            "startDateTime": "2023-12-01T08:00:00Z",
        }
        result = self.client.security.attack_simulation.simulations.add(**simulation).execute_query()
        self.assertIsNotNone(result.resource_path)

    @requires_application("SecurityIncident.Read.All", "SecurityIncident.ReadWrite.All")
    def test2_list_incidents(self):
        """List security incidents."""
        col = self.client.security.incidents.top(10).get().execute_query()
        self.assertIsNotNone(col.resource_path)

    # def test3_list_landing_pages(self):
    #    col = (
    #        self.client.security.attack_simulation.landing_pages.filter("source eq 'tenant'")
    #        .get()
    #        .execute_query()
    #    )
    #    self.assertIsNotNone(col.resource_path)
