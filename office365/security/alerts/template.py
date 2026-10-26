from __future__ import annotations

from dataclasses import dataclass, field

from office365.runtime.client_value import ClientValue
from office365.runtime.client_value_collection import ClientValueCollection
from office365.security.alerts.custom_details import AlertCustomDetails
from office365.security.alerts.severity import AlertSeverity
from office365.security.entity_mapping_configuration import EntityMappingConfiguration
from office365.security.mitre_tactic import MitreTactic


@dataclass
class AlertTemplate(ClientValue):
    customDetails: AlertCustomDetails = field(default_factory=AlertCustomDetails)
    description: str | None = None
    entityMappings: EntityMappingConfiguration = field(default_factory=EntityMappingConfiguration)
    recommendedActions: str | None = None
    severity: AlertSeverity = AlertSeverity.unknown
    tactics: ClientValueCollection[MitreTactic] = field(default_factory=lambda: ClientValueCollection(MitreTactic))
    title: str | None = None

    @property
    def entity_type_name(self) -> str:
        return "microsoft.graph.security.AlertTemplate"
