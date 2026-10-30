from __future__ import annotations

from office365.entity import Entity
from office365.runtime.types.odata_property import odata
from office365.security.sensor_candidate_activation_mode import SensorCandidateActivationMode


class SensorCandidateActivationConfiguration(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SensorCandidateActivationConfiguration"

    @odata(name="activationMode")
    @property
    def activation_mode(self) -> SensorCandidateActivationMode:
        """Gets the activationMode property"""
        return self.properties.get("activationMode", SensorCandidateActivationMode.manual)
