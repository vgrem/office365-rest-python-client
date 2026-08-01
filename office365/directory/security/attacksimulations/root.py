from office365.directory.security.attacksimulations.automation import (
    SimulationAutomation,
)
from office365.directory.security.attacksimulations.landing_page import LandingPage
from office365.directory.security.attacksimulations.operations.operation import (
    AttackSimulationOperation,
)
from office365.directory.security.attacksimulations.simulation import Simulation
from office365.entity import Entity
from office365.entity_collection import EntityCollection
from office365.runtime.paths.resource_path import ResourcePath
from office365.runtime.types.odata_property import odata


class AttackSimulationRoot(Entity):
    """Represents an abstract type that provides the ability to launch a realistic phishing attack that organizations
    can learn from."""

    @odata(name="landingPages")
    @property
    def landing_pages(self) -> EntityCollection[LandingPage]:
        """Represents an attack simulation training landing page."""
        return self.properties.get(
            "landingPages",
            EntityCollection(
                self.context,
                LandingPage,
                ResourcePath("landingPages", self.resource_path),
            ),
        )

    @property
    def operations(self) -> EntityCollection[AttackSimulationOperation]:
        """Represents an attack simulation training operation."""
        return self.properties.get(
            "operations",
            EntityCollection(
                self.context,
                AttackSimulationOperation,
                ResourcePath("operations", self.resource_path),
            ),
        )

    @property
    def simulations(self) -> EntityCollection[Simulation]:
        """Represents an attack simulation training campaign in a tenant."""
        return self.properties.get(
            "simulations",
            EntityCollection(
                self.context,
                Simulation,
                ResourcePath("simulations", self.resource_path),
            ),
        )

    @odata(name="simulationAutomations")
    @property
    def simulation_automations(self) -> EntityCollection[SimulationAutomation]:
        """Represents simulation automation created to run on a tenant."""
        return self.properties.get(
            "simulationAutomations",
            EntityCollection(
                self.context,
                SimulationAutomation,
                ResourcePath("simulationAutomations", self.resource_path),
            ),
        )
