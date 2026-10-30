from __future__ import annotations

from typing import TYPE_CHECKING

from office365.entity import Entity
from office365.runtime.types.odata_property import odata

if TYPE_CHECKING:
    from office365.security.sensor_candidate_activation_mode import (
        SensorCandidateActivationMode,
    )


class SensorCandidateActivationConfiguration(Entity):
    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.SensorCandidateActivationConfiguration"

    @odata(name="activationMode")
    @property
    def activation_mode(self) -> SensorCandidateActivationMode:
        """Gets the activationMode property"""
        from office365.security.sensor_candidate_activation_mode import (
            SensorCandidateActivationMode,
        )

        return self.properties.get("activationMode", SensorCandidateActivationMode.manual)
