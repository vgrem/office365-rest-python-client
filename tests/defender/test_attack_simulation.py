"""Attack Simulation & Training — simulating phishing attacks and tracking user training.
Tests cover:
  - Listing simulations, landing pages, and training modules
  - Filtering simulations by status and technique
  - Creating a new simulation campaign
  - Listing simulation automations
  - Accessing simulation reports (repeat offenders, user coverage)
  - Landing page and payload retrieval
"""
from __future__ import annotations
from typing import ClassVar, Optional
from tests.decorators import requires_delegated, requires_application
from tests.graph_case import GraphDelegatedTestCase
_SIM_READ = ("AttackSimulation.Read.All",)
_SIM_WRITE = ("AttackSimulation.ReadWrite.All",)
class TestAttackSimulationList(GraphDelegatedTestCase):
    """Listing and discovering attack simulation resources."""
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_01_list_simulations(self):
        """Listing attack simulations returns a valid collection."""
        result = self.client.security.attack_simulation.simulations.top(10).get().execute_query()
        self.assertIsNotNone(result.resource_path)
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_02_list_simulation_automations(self):
        """Listing simulation automations returns a valid collection."""
        result = (
            self.client.security.attack_simulation.simulation_automations.top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_03_list_landing_pages(self):
        """Listing attack simulation landing pages returns a valid collection."""
        result = self.client.security.attack_simulation.landing_pages.top(5).get().execute_query()
        self.assertIsNotNone(result.resource_path)
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_04_filter_simulations_by_status(self):
        """Filtering simulations by status works correctly."""
        result = (
            self.client.security.attack_simulation.simulations.filter("status eq 'completed'")
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for sim in result:
            self.assertEqual(sim.get_property("status"), "completed")
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_05_filter_simulations_by_technique(self):
        """Filtering simulations by attack technique returns matching results."""
        result = (
            self.client.security.attack_simulation.simulations.filter(
                "attackTechnique eq 'credentialHarvesting'"
            )
            .top(5)
            .get()
            .execute_query()
        )
        self.assertIsNotNone(result.resource_path)
        for sim in result:
            technique = sim.get_property("attackTechnique")
            self.assertEqual(technique, "credentialHarvesting")
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_06_simulation_has_required_properties(self):
        """A simulation exposes displayName, status, attackTechnique, and createdDateTime."""
        result = self.client.security.attack_simulation.simulations.top(3).get().execute_query()
        if len(result) == 0:
            self.skipTest("No simulations exist to inspect")
        for sim in result:
            self.assertIsNotNone(sim.get_property("displayName"))
            self.assertIsNotNone(sim.get_property("status"))
            self.assertIsNotNone(sim.get_property("attackTechnique"))
            self.assertIsNotNone(sim.get_property("createdDateTime"))
            break
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_07_landing_page_has_display_name(self):
        """A landing page exposes a displayName and status."""
        result = self.client.security.attack_simulation.landing_pages.top(3).get().execute_query()
        if len(result) == 0:
            self.skipTest("No landing pages exist")
        for page in result:
            self.assertIsNotNone(page.get_property("displayName"))
            self.assertIsNotNone(page.get_property("status"))
            break
    @requires_delegated(
        *_SIM_READ,
        bypass_roles=["Global Administrator"],
    )
    def test_08_list_operations(self):
        """Listing attack simulation operations returns a valid collection."""
        result = self.client.security.attack_simulation.operations.top(5).get().execute_query()
        self.assertIsNotNone(result.resource_path)
class TestAttackSimulationCreate(GraphDelegatedTestCase):
    """Creating attack simulations — requires app-level auth or appropriate delegated permissions."""
    created_sim: ClassVar[Optional[object]] = None
    @requires_application(*_SIM_WRITE)
    def test_01_create_simulation(self):
        """Creating an attack simulation campaign with credentialHarvesting technique."""
        sim_name = f"SDK Test — Automated Campaign ({id(self)})"
        simulation = {
            "displayName": sim_name,
            "payloadDeliveryPlatform": "email",
            "durationInDays": 3,
            "attackTechnique": "credentialHarvesting",
            "status": "scheduled",
            "startDateTime": "2026-07-01T08:00:00Z",
        }
        result = self.client.security.attack_simulation.simulations.add(**simulation).execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("displayName"), sim_name)
        self.assertEqual(result.get_property("attackTechnique"), "credentialHarvesting")
        TestAttackSimulationCreate.created_sim = result
    @requires_application(*_SIM_WRITE)
    def test_02_get_created_simulation(self):
        """Retrieving a simulation by ID returns the expected object."""
        created = TestAttackSimulationCreate.created_sim
        if not created:
            self.skipTest("No created simulation from previous test")
        result = self.client.security.attack_simulation.simulations[created.id].get().execute_query()
        self.assertIsNotNone(result.resource_path)
        self.assertEqual(result.get_property("id"), created.id)
    @classmethod
    def tearDownClass(cls):
        """Best-effort cleanup."""
        sim = cls.created_sim
        if sim and sim.resource_path:
            try:
                sim.delete_object().execute_query()
            except Exception:
                pass
